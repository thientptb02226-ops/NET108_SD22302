import { Router, Request, Response } from 'express';
import prisma from '../lib/prisma';
import { authenticateToken, requireRole } from '../middleware/auth';

const router = Router();

// Require Merchant or SuperAdmin for all admin routes
router.use(authenticateToken, requireRole('Merchant', 'SuperAdmin'));

// GET /api/v1/admin/dashboard (Analytics & KPI Overview)
router.get('/dashboard', async (_req: Request, res: Response) => {
  try {
    const [totalUsers, totalProducts, totalOrders, orders] = await Promise.all([
      prisma.user.count({ where: { status: 'ACTIVE' } }),
      prisma.product.count({ where: { status: 'ACTIVE' } }),
      prisma.order.count(),
      prisma.order.findMany({
        select: { finalAmountMinor: true, status: true, paymentStatus: true, createdAt: true },
        orderBy: { createdAt: 'desc' }
      })
    ]);

    const totalRevenueMinor = orders
      .filter((o) => o.paymentStatus === 'PAID')
      .reduce((sum, o) => sum + o.finalAmountMinor, 0);

    const pendingOrdersCount = orders.filter((o) => o.status === 'PENDING').length;
    const completedOrdersCount = orders.filter((o) => o.status === 'COMPLETED' || o.status === 'CONFIRMED').length;

    // Recent 5 days revenue mock aggregation
    const revenueByDay = [
      { date: '04/11', revenue: 15400000 },
      { date: '05/11', revenue: 22800000 },
      { date: '06/11', revenue: 34490000 },
      { date: '07/11', revenue: 28900000 },
      { date: '08/11', revenue: totalRevenueMinor }
    ];

    res.json({
      metrics: {
        totalRevenueMinor,
        totalOrders,
        pendingOrdersCount,
        completedOrdersCount,
        totalProducts,
        totalUsers
      },
      revenueByDay
    });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi tải thống kê dashboard' });
  }
});

// PUT /api/v1/admin/orders/:id/status (Transition Order State in Waterfall)
router.put('/orders/:id/status', async (req: Request, res: Response) => {
  try {
    const id = Number(req.params.id);
    const { status, trackingNumber } = req.body;

    const validStatuses = ['PENDING', 'CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'COMPLETED', 'CANCELLED'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({ error: 'INVALID_STATUS', message: 'Trạng thái đơn hàng không hợp lệ' });
    }

    const updated = await prisma.order.update({
      where: { id },
      data: {
        status,
        ...(status === 'DELIVERED' || status === 'COMPLETED' ? { paymentStatus: 'PAID' } : {}),
        shippingRecord: trackingNumber
          ? {
              update: {
                trackingNumber,
                shippingStatus: status === 'SHIPPED' ? 'IN_TRANSIT' : 'DELIVERED'
              }
            }
          : undefined
      },
      include: { shippingRecord: true }
    });

    // Record Audit Log
    await prisma.auditLog.create({
      data: {
        userId: req.user!.id,
        actorType: req.user!.roleName,
        action: 'UPDATE_ORDER_STATUS',
        entityName: 'orders',
        entityId: String(id),
        details: JSON.stringify({ newStatus: status, admin: req.user!.fullName })
      }
    });

    res.json({ message: 'Cập nhật trạng thái đơn hàng thành công', order: updated });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi cập nhật trạng thái đơn hàng' });
  }
});

// GET /api/v1/admin/audit-logs
router.get('/audit-logs', async (_req: Request, res: Response) => {
  try {
    const logs = await prisma.auditLog.findMany({
      take: 50,
      orderBy: { createdAt: 'desc' },
      include: { user: { select: { fullName: true, email: true } } }
    });
    res.json({ logs });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi tải nhật ký kiểm toán' });
  }
});

export default router;
