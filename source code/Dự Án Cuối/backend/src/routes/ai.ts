import { Router, Request, Response } from 'express';
import prisma from '../lib/prisma';
import { authenticateToken } from '../middleware/auth';

const router = Router();

// POST /api/v1/ai/nlp-search (Natural Language Semantic Search)
router.post('/nlp-search', async (req: Request, res: Response) => {
  try {
    const { query } = req.body;
    if (!query || typeof query !== 'string') {
      return res.status(400).json({ error: 'INVALID_QUERY', message: 'Vui lòng cung cấp câu truy vấn tìm kiếm' });
    }

    const qLower = query.toLowerCase();

    // 1. Intent extraction
    let maxPriceMinor: number | null = null;
    if (qLower.includes('dưới 35 triệu') || qLower.includes('duoi 35tr') || qLower.includes('< 35tr')) {
      maxPriceMinor = 35000000;
    } else if (qLower.includes('dưới 10 triệu') || qLower.includes('duoi 10tr')) {
      maxPriceMinor = 10000000;
    } else if (qLower.includes('dưới 50 triệu')) {
      maxPriceMinor = 50000000;
    }

    // 2. Keyword tokens
    const tokens = qLower
      .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '')
      .split(/\s+/)
      .filter((w) => w.length > 1);

    // 3. Fetch products
    const allProducts = await prisma.product.findMany({
      where: { status: 'ACTIVE' },
      include: { category: true }
    });

    // 4. Semantic ranking algorithm
    const scoredProducts = allProducts.map((p) => {
      let score = 0;
      const textCorpus = `${p.name} ${p.description || ''} ${p.aiTags || ''} ${p.category.name}`.toLowerCase();

      for (const token of tokens) {
        if (textCorpus.includes(token)) score += 3;
      }

      // Check specific semantic concepts
      if (qLower.includes('mỏng nhẹ') && textCorpus.includes('mong-nhe')) score += 5;
      if (qLower.includes('pin trâu') && textCorpus.includes('pin-trau')) score += 5;
      if (qLower.includes('gaming') && textCorpus.includes('gaming')) score += 5;
      if (qLower.includes('học tập') || qLower.includes('sinh viên')) {
        if (textCorpus.includes('hoc-tap') || textCorpus.includes('van-phong')) score += 4;
      }
      if (qLower.includes('tai nghe') && p.categoryId === 2) score += 5;
      if (qLower.includes('cà phê') || qLower.includes('cafe')) {
        if (p.categoryId === 4) score += 6;
      }

      // Price filter penalty
      if (maxPriceMinor && p.priceMinor > maxPriceMinor) {
        score -= 10;
      }

      return {
        product: {
          ...p,
          specs: p.specs ? JSON.parse(p.specs) : null,
          aiTags: p.aiTags ? JSON.parse(p.aiTags) : []
        },
        score
      };
    });

    const results = scoredProducts
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 6);

    res.json({
      query,
      detectedIntent: {
        maxPriceMinor,
        keywords: tokens,
        category: results.length > 0 ? results[0].product.category.name : 'Tất cả'
      },
      matchCount: results.length,
      results: results.map((r) => ({
        ...r.product,
        matchScore: r.score,
        aiExplanation: `Phù hợp với nhu cầu '${query}' nhờ thuộc tính ${r.product.aiTags?.slice(0, 3).join(', ')}`
      }))
    });
  } catch (error) {
    console.error('NLP search error:', error);
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi tìm kiếm ngôn ngữ tự nhiên' });
  }
});

// POST /api/v1/ai/assistant/chat (Conversational Shopping Assistant)
router.post('/assistant/chat', async (req: Request, res: Response) => {
  try {
    const { message, history = [] } = req.body;
    if (!message) {
      return res.status(400).json({ error: 'INVALID_MESSAGE', message: 'Nội dung tin nhắn không được để trống' });
    }

    const msgLower = message.toLowerCase();

    // Query relevant products to recommend
    const products = await prisma.product.findMany({
      where: { status: 'ACTIVE' },
      take: 4,
      include: { category: true }
    });

    let reply = '';
    let suggestedProducts: any[] = [];
    let voucherRecommendation: string | null = null;

    if (msgLower.includes('laptop') || msgLower.includes('máy tính')) {
      const laptop = products.find((p) => p.categoryId === 1);
      suggestedProducts = products.filter((p) => p.categoryId === 1);
      reply = `Dạ chào bạn! Để phục vụ học tập, lập trình và văn phòng mỏng nhẹ, AI Assistant gợi ý bạn tham khảo **${laptop?.name || 'MacBook Air M3'}** với thời lượng pin lên đến 18 giờ và chip Apple M3 Neural Engine xử lý AI siêu mượt.`;
      voucherRecommendation = 'AINATIVE2026 (Giảm ngay 1.000.000đ cho đơn từ 30 triệu)';
    } else if (msgLower.includes('điện thoại') || msgLower.includes('iphone')) {
      suggestedProducts = products.filter((p) => p.categoryId === 2 && p.name.includes('iPhone'));
      reply = `Chào bạn! Hiện bên mình đang có siêu phẩm **iPhone 16 Pro Max 256GB Titan Tự Nhiên** hỗ trợ Apple Intelligence cực đỉnh, camera điều khiển cảm ứng lực thế hệ mới!`;
    } else if (msgLower.includes('cà phê') || msgLower.includes('cafe')) {
      suggestedProducts = products.filter((p) => p.categoryId === 4);
      reply = `Dạ nếu bạn cần sự tập trung cho một ngày làm việc tràn đầy năng lượng, dòng **Cà Phê Arabica Cầu Đất 100% Rang Mộc** với hương caramel & trái cây dịu nhẹ là sự lựa chọn tuyệt vời ạ!`;
    } else if (msgLower.includes('khuyến mãi') || msgLower.includes('voucher') || msgLower.includes('giảm giá')) {
      reply = `Hiện hệ thống AI-Native Commerce đang có chương trình khuyến mãi tự động:\n- Mã **AINATIVE2026**: Giảm 5% (tối đa 1.000.000đ) cho đơn hàng từ 30.000.000đ.\n- Miễn phí vận chuyển toàn quốc cho đơn từ 500.000đ khi thanh toán qua VNPay/VietQR!`;
      voucherRecommendation = 'AINATIVE2026';
    } else {
      suggestedProducts = products.slice(0, 2);
      reply = `Chào bạn! Mình là AI Shopping Assistant của nền tảng AI-Native Commerce. Mình có thể giúp bạn tìm kiếm sản phẩm theo ngôn ngữ tự nhiên, so sánh cấu hình, tư vấn chọn mua và tự động áp dụng mã giảm giá tối ưu nhất. Bạn đang quan tâm đến sản phẩm nào ạ?`;
    }

    res.json({
      reply,
      suggestedProducts: suggestedProducts.map((p) => ({
        id: p.id,
        name: p.name,
        priceMinor: p.priceMinor,
        imageUrl: p.imageUrl,
        sku: p.sku
      })),
      voucherRecommendation
    });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi trợ lý hội thoại AI' });
  }
});

// GET /api/v1/ai/approvals (Human-in-the-loop Approvals)
router.get('/approvals', authenticateToken, async (req: Request, res: Response) => {
  try {
    const approvals = await prisma.aiActionApproval.findMany({
      orderBy: { createdAt: 'desc' }
    });
    res.json({ approvals });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi tải danh sách phê duyệt AI' });
  }
});

export default router;
