import { Router, Request, Response } from 'express';
import prisma from '../lib/prisma';
import { authenticateToken } from '../middleware/auth';

const router = Router();

// GET /api/v1/orders
router.get('/', authenticateToken, async (req: Request, res: Response) => {
  try {
    const userId = req.user!.id;
    const isStaff = req.user!.roleName === 'Merchant' || req.user!.roleName === 'SuperAdmin';

    const where = isStaff ? {} : { userId };

    const orders = await prisma.order.findMany({
      where,
      include: {
        items: { include: { product: true } },
        payments: true,
        shippingRecord: true,
        user: { select: { fullName: true, email: true, phone: true } }
      },
      orderBy: { createdAt: 'desc' }
    });

    res.json({ orders });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi tải danh sách đơn hàng' });
  }
});

// GET /api/v1/orders/:id
router.get('/:id', authenticateToken, async (req: Request, res: Response) => {
  try {
    const id = Number(req.params.id);
    const userId = req.user!.id;
    const isStaff = req.user!.roleName === 'Merchant' || req.user!.roleName === 'SuperAdmin';

    const order = await prisma.order.findUnique({
      where: { id },
      include: {
        items: { include: { product: true } },
        payments: true,
        shippingRecord: true,
        user: { select: { fullName: true, email: true, phone: true } }
      }
    });

    if (!order) {
      return res.status(404).json({ error: 'NOT_FOUND', message: 'Không tìm thấy đơn hàng' });
    }

    if (!isStaff && order.userId !== userId) {
      return res.status(403).json({ error: 'FORBIDDEN', message: 'Bạn không có quyền xem đơn hàng này' });
    }

    res.json({ order });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi tải chi tiết đơn hàng' });
  }
});

// POST /api/v1/orders/:id/cancel
router.post('/:id/cancel', authenticateToken, async (req: Request, res: Response) => {
  try {
    const id = Number(req.params.id);
    const userId = req.user!.id;

    const order = await prisma.order.findUnique({
      where: { id },
      include: { items: true }
    });

    if (!order) {
      return res.status(404).json({ error: 'NOT_FOUND', message: 'Không tìm thấy đơn hàng' });
    }

    if (order.userId !== userId && req.user!.roleName === 'Customer') {
      return res.status(403).json({ error: 'FORBIDDEN', message: 'Không thể hủy đơn hàng của người khác' });
    }

    if (!['PENDING', 'CONFIRMED'].includes(order.status)) {
      return res.status(400).json({
        error: 'CANNOT_CANCEL',
        message: `Đơn hàng đang ở trạng thái '${order.status}', không thể hủy trực tiếp.`
      });
    }

    // Cancel order and restock
    await prisma.$transaction(async (tx) => {
      await tx.order.update({
        where: { id },
        data: { status: 'CANCELLED' }
      });

      for (const item of order.items) {
        await tx.product.update({
          where: { id: item.productId },
          data: { stockQuantity: { increment: item.quantity } }
        });
      }

      await tx.auditLog.create({
        data: {
          userId,
          action: 'CANCEL_ORDER',
          entityName: 'orders',
          entityId: String(id),
          details: JSON.stringify({ reason: 'Khách hàng yêu cầu hủy đơn' })
        }
      });
    });

    res.json({ message: 'Hủy đơn hàng thành công, tồn kho đã được hoàn trả.' });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi khi hủy đơn hàng' });
  }
});

export default router;
