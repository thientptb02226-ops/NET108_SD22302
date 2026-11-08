import { Router, Request, Response } from 'express';
import { z } from 'zod';
import prisma from '../lib/prisma';
import { authenticateToken } from '../middleware/auth';
import { handleIdempotency } from '../middleware/idempotency';

const router = Router();

const checkoutConfirmSchema = z.object({
  quoteId: z.string().uuid(),
  shippingName: z.string().min(2),
  shippingPhone: z.string().min(8),
  shippingAddress: z.string().min(5),
  paymentMethod: z.enum(['VNPAY', 'MOMO', 'VIETQR', 'COD']),
  notes: z.string().optional()
});

// POST /api/v1/checkout/confirm (Executes Checkout Saga with Idempotency)
router.post(
  '/confirm',
  authenticateToken,
  handleIdempotency('CHECKOUT_CONFIRM'),
  async (req: Request, res: Response) => {
    try {
      const userId = req.user!.id;
      const body = checkoutConfirmSchema.parse(req.body);

      // 1. Validate Quote
      const quote = await prisma.quote.findUnique({
        where: { id: body.quoteId },
        include: {
          cart: {
            include: {
              items: { include: { product: true } }
            }
          }
        }
      });

      if (!quote) {
        return res.status(404).json({ error: 'QUOTE_NOT_FOUND', message: 'Báo giá checkout không tồn tại' });
      }

      if (quote.customerId !== userId) {
        return res.status(403).json({ error: 'FORBIDDEN', message: 'Báo giá này không thuộc tài khoản của bạn' });
      }

      if (new Date() > quote.expiresAt) {
        return res.status(400).json({ error: 'QUOTE_EXPIRED', message: 'Báo giá đã hết hạn (quá 15 phút), vui lòng quay lại giỏ hàng' });
      }

      if (!quote.cart.items || quote.cart.items.length === 0) {
        return res.status(400).json({ error: 'EMPTY_CART', message: 'Giỏ hàng không có sản phẩm để đặt' });
      }

      // 2. Check & Reserve Inventory (Hold Stock)
      for (const item of quote.cart.items) {
        if (item.product.stockQuantity < item.quantity) {
          return res.status(400).json({
            error: 'OUT_OF_STOCK',
            message: `Sản phẩm '${item.product.name}' chỉ còn ${item.product.stockQuantity} sản phẩm trong kho.`
          });
        }
      }

      // Generate Order Code: ORD-YYYYMMDD-XXXX
      const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
      const randomSuffix = Math.floor(1000 + Math.random() * 9000);
      const orderCode = `ORD-${dateStr}-${randomSuffix}`;

      // 3. Create Order in Transaction
      const order = await prisma.$transaction(async (tx) => {
        // Create Inventory Reservation
        for (const item of quote.cart.items) {
          await tx.inventoryReservation.create({
            data: {
              quoteId: quote.id,
              productId: item.productId,
              quantity: item.quantity,
              status: 'CONSUMED',
              expiresAt: new Date(Date.now() + 30 * 60 * 1000)
            }
          });

          // Deduct product stock
          await tx.product.update({
            where: { id: item.productId },
            data: { stockQuantity: { decrement: item.quantity } }
          });
        }

        // Create Order
        const newOrder = await tx.order.create({
          data: {
            userId,
            quoteId: quote.id,
            orderCode,
            totalMinor: quote.subtotalMinor,
            discountMinor: quote.discountMinor,
            shippingMinor: quote.shippingMinor,
            finalAmountMinor: quote.totalMinor,
            status: body.paymentMethod === 'COD' ? 'CONFIRMED' : 'PENDING',
            paymentStatus: body.paymentMethod === 'COD' ? 'UNPAID' : 'PAID', // Demo payment immediate approval
            shippingName: body.shippingName,
            shippingPhone: body.shippingPhone,
            shippingAddress: body.shippingAddress,
            notes: body.notes,
            items: {
              create: quote.cart.items.map((it) => ({
                productId: it.productId,
                quantity: it.quantity,
                unitPriceMinor: it.unitPriceMinor,
                subtotalMinor: it.quantity * it.unitPriceMinor
              }))
            },
            payments: {
              create: {
                paymentMethod: body.paymentMethod,
                transactionId: `TX-${Date.now()}-${randomSuffix}`,
                amountMinor: quote.totalMinor,
                status: body.paymentMethod === 'COD' ? 'PENDING' : 'PAID'
              }
            },
            shippingRecord: {
              create: {
                carrierCode: 'GHN',
                trackingNumber: `GHN-${dateStr}-${randomSuffix}`,
                shippingStatus: 'READY_TO_PICK',
                estimatedDelivery: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000)
              }
            }
          },
          include: {
            items: { include: { product: true } },
            payments: true,
            shippingRecord: true
          }
        });

        // Clear Cart Items
        await tx.cartItem.deleteMany({
          where: { cartId: quote.cartId }
        });

        // Audit Log
        await tx.auditLog.create({
          data: {
            userId,
            actorType: 'User',
            action: 'CREATE_ORDER',
            entityName: 'orders',
            entityId: String(newOrder.id),
            details: JSON.stringify({ orderCode, total: quote.totalMinor, paymentMethod: body.paymentMethod })
          }
        });

        return newOrder;
      });

      res.status(201).json({
        message: 'Đặt hàng thành công!',
        order: {
          id: order.id,
          orderCode: order.orderCode,
          status: order.status,
          paymentStatus: order.paymentStatus,
          finalAmountMinor: order.finalAmountMinor,
          shippingAddress: order.shippingAddress,
          trackingNumber: order.shippingRecord?.trackingNumber,
          createdAt: order.createdAt
        }
      });
    } catch (error: any) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ error: 'VALIDATION_ERROR', details: error.errors });
      }
      console.error('Checkout confirm error:', error);
      res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi thực thi quy trình đặt hàng' });
    }
  }
);

export default router;
