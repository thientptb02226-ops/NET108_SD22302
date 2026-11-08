import { Router, Request, Response } from 'express';
import crypto from 'crypto';
import prisma from '../lib/prisma';
import { authenticateToken } from '../middleware/auth';

const router = Router();

// GET /api/v1/carts
router.get('/', authenticateToken, async (req: Request, res: Response) => {
  try {
    const userId = req.user!.id;

    let cart = await prisma.cart.findFirst({
      where: { userId },
      include: {
        items: {
          include: { product: true }
        }
      }
    });

    if (!cart) {
      cart = await prisma.cart.create({
        data: { userId },
        include: {
          items: {
            include: { product: true }
          }
        }
      });
    }

    const totalMinor = cart.items.reduce(
      (sum, item) => sum + item.quantity * item.unitPriceMinor,
      0
    );

    res.json({
      cart: {
        ...cart,
        totalMinor
      }
    });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi tải giỏ hàng' });
  }
});

// POST /api/v1/carts/items
router.post('/items', authenticateToken, async (req: Request, res: Response) => {
  try {
    const userId = req.user!.id;
    const { productId, quantity = 1 } = req.body;

    const product = await prisma.product.findUnique({
      where: { id: Number(productId) }
    });

    if (!product || product.status !== 'ACTIVE') {
      return res.status(404).json({ error: 'PRODUCT_NOT_AVAILABLE', message: 'Sản phẩm không tồn tại hoặc đã ngừng kinh doanh' });
    }

    if (product.stockQuantity < quantity) {
      return res.status(400).json({
        error: 'OUT_OF_STOCK',
        message: `Số lượng yêu cầu (${quantity}) vượt quá tồn kho khả dụng (${product.stockQuantity})`
      });
    }

    let cart = await prisma.cart.findFirst({ where: { userId } });
    if (!cart) {
      cart = await prisma.cart.create({ data: { userId } });
    }

    const existingItem = await prisma.cartItem.findUnique({
      where: {
        cartId_productId: {
          cartId: cart.id,
          productId: product.id
        }
      }
    });

    if (existingItem) {
      await prisma.cartItem.update({
        where: { id: existingItem.id },
        data: {
          quantity: existingItem.quantity + quantity,
          unitPriceMinor: product.priceMinor
        }
      });
    } else {
      await prisma.cartItem.create({
        data: {
          cartId: cart.id,
          productId: product.id,
          quantity,
          unitPriceMinor: product.priceMinor
        }
      });
    }

    // Refresh cart
    const updatedCart = await prisma.cart.findUnique({
      where: { id: cart.id },
      include: { items: { include: { product: true } } }
    });

    const totalMinor = updatedCart!.items.reduce(
      (sum, item) => sum + item.quantity * item.unitPriceMinor,
      0
    );

    res.json({
      message: 'Đã thêm sản phẩm vào giỏ hàng',
      cart: { ...updatedCart, totalMinor }
    });
  } catch (error) {
    console.error('Cart add error:', error);
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi thêm sản phẩm vào giỏ hàng' });
  }
});

// DELETE /api/v1/carts/items/:id
router.delete('/items/:id', authenticateToken, async (req: Request, res: Response) => {
  try {
    const itemId = Number(req.params.id);
    await prisma.cartItem.delete({
      where: { id: itemId }
    });
    res.json({ message: 'Đã xóa sản phẩm khỏi giỏ hàng' });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi xóa sản phẩm khỏi giỏ hàng' });
  }
});

// POST /api/v1/carts/quote (Lock Price & Generate Quote according to ChatGPT Specification)
router.post('/quote', authenticateToken, async (req: Request, res: Response) => {
  try {
    const userId = req.user!.id;
    const { voucherCode } = req.body;

    const cart = await prisma.cart.findFirst({
      where: { userId },
      include: { items: { include: { product: true } } }
    });

    if (!cart || cart.items.length === 0) {
      return res.status(400).json({ error: 'EMPTY_CART', message: 'Giỏ hàng đang trống' });
    }

    const subtotalMinor = cart.items.reduce(
      (sum, item) => sum + item.quantity * item.unitPriceMinor,
      0
    );

    // AI Promotion auto-matcher
    let discountMinor = 0;
    if (voucherCode === 'AINATIVE2026' || subtotalMinor > 30000000) {
      discountMinor = Math.min(1000000, Math.floor(subtotalMinor * 0.05)); // 5% up to 1M VND
    }

    const shippingMinor = subtotalMinor > 500000 ? 0 : 30000; // Free shipping over 500k
    const taxMinor = 0; // VAT included in prices in Vietnam
    const totalMinor = subtotalMinor - discountMinor + shippingMinor + taxMinor;

    const expiresAt = new Date(Date.now() + 15 * 60 * 1000); // Quote valid for 15 minutes
    const fingerprintPayload = `${userId}:${cart.id}:${subtotalMinor}:${discountMinor}:${shippingMinor}:${totalMinor}`;
    const fingerprint = crypto.createHash('sha256').update(fingerprintPayload).digest('hex');

    const quote = await prisma.quote.create({
      data: {
        customerId: userId,
        cartId: cart.id,
        subtotalMinor,
        discountMinor,
        shippingMinor,
        taxMinor,
        totalMinor,
        fingerprint,
        expiresAt
      }
    });

    res.json({
      quote: {
        id: quote.id,
        subtotalMinor: quote.subtotalMinor,
        discountMinor: quote.discountMinor,
        shippingMinor: quote.shippingMinor,
        totalMinor: quote.totalMinor,
        fingerprint: quote.fingerprint,
        expiresAt: quote.expiresAt,
        itemsCount: cart.items.length
      }
    });
  } catch (error) {
    console.error('Create quote error:', error);
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi khởi tạo báo giá checkout' });
  }
});

export default router;
