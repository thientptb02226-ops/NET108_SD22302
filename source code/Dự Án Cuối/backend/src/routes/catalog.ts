import { Router, Request, Response } from 'express';
import { z } from 'zod';
import prisma from '../lib/prisma';
import { authenticateToken, requireRole } from '../middleware/auth';

const router = Router();

// GET /api/v1/catalog/categories
router.get('/categories', async (_req: Request, res: Response) => {
  try {
    const categories = await prisma.category.findMany({
      where: { active: true },
      include: {
        _count: { select: { products: true } }
      }
    });
    res.json({ categories });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi tải danh mục sản phẩm' });
  }
});

// GET /api/v1/catalog/products
router.get('/products', async (req: Request, res: Response) => {
  try {
    const { categoryId, q, tag, minPrice, maxPrice, page = '1', limit = '12' } = req.query;

    const where: any = { status: 'ACTIVE' };

    if (categoryId) {
      where.categoryId = Number(categoryId);
    }

    if (q) {
      where.OR = [
        { name: { contains: String(q) } },
        { description: { contains: String(q) } },
        { sku: { contains: String(q) } }
      ];
    }

    if (tag) {
      where.aiTags = { contains: String(tag) };
    }

    if (minPrice || maxPrice) {
      where.priceMinor = {};
      if (minPrice) where.priceMinor.gte = Number(minPrice);
      if (maxPrice) where.priceMinor.lte = Number(maxPrice);
    }

    const take = Number(limit);
    const skip = (Number(page) - 1) * take;

    const [products, total] = await Promise.all([
      prisma.product.findMany({
        where,
        take,
        skip,
        include: { category: true },
        orderBy: { createdAt: 'desc' }
      }),
      prisma.product.count({ where })
    ]);

    // Format products (parse JSON specs and aiTags)
    const formatted = products.map((p) => ({
      ...p,
      specs: p.specs ? JSON.parse(p.specs) : null,
      aiTags: p.aiTags ? JSON.parse(p.aiTags) : []
    }));

    res.json({
      products: formatted,
      pagination: {
        total,
        page: Number(page),
        limit: take,
        totalPages: Math.ceil(total / take)
      }
    });
  } catch (error) {
    console.error('Fetch products error:', error);
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi tải danh sách sản phẩm' });
  }
});

// GET /api/v1/catalog/products/:id
router.get('/products/:id', async (req: Request, res: Response) => {
  try {
    const id = Number(req.params.id);
    const product = await prisma.product.findUnique({
      where: { id },
      include: {
        category: true,
        vector: { select: { embeddingModel: true, updatedAt: true } }
      }
    });

    if (!product) {
      return res.status(404).json({ error: 'NOT_FOUND', message: 'Không tìm thấy sản phẩm' });
    }

    res.json({
      product: {
        ...product,
        specs: product.specs ? JSON.parse(product.specs) : null,
        galleryUrls: product.galleryUrls ? JSON.parse(product.galleryUrls) : [],
        aiTags: product.aiTags ? JSON.parse(product.aiTags) : []
      }
    });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi tải thông tin sản phẩm' });
  }
});

// POST /api/v1/catalog/products (Merchant/Admin)
router.post(
  '/products',
  authenticateToken,
  requireRole('Merchant', 'SuperAdmin'),
  async (req: Request, res: Response) => {
    try {
      const productSchema = z.object({
        categoryId: z.number(),
        name: z.string().min(2),
        sku: z.string().min(3),
        priceMinor: z.number().positive(),
        originalPriceMinor: z.number().optional(),
        stockQuantity: z.number().nonnegative(),
        description: z.string().optional(),
        specs: z.record(z.any()).optional(),
        imageUrl: z.string().url().optional(),
        aiTags: z.array(z.string()).optional()
      });

      const body = productSchema.parse(req.body);

      const newProduct = await prisma.product.create({
        data: {
          categoryId: body.categoryId,
          name: body.name,
          sku: body.sku,
          priceMinor: body.priceMinor,
          originalPriceMinor: body.originalPriceMinor,
          stockQuantity: body.stockQuantity,
          description: body.description,
          specs: body.specs ? JSON.stringify(body.specs) : null,
          imageUrl: body.imageUrl,
          aiTags: body.aiTags ? JSON.stringify(body.aiTags) : '[]'
        },
        include: { category: true }
      });

      // Auto create vector record for AI search
      const mockVector = Array.from({ length: 16 }, () => Number((Math.random() * 2 - 1).toFixed(4)));
      await prisma.productVector.create({
        data: {
          productId: newProduct.id,
          embeddingModel: 'text-embedding-3-small',
          embeddingVector: JSON.stringify(mockVector),
          metadataJson: JSON.stringify({ category: newProduct.categoryId, name: newProduct.name })
        }
      });

      res.status(201).json({
        message: 'Thêm mới sản phẩm thành công',
        product: newProduct
      });
    } catch (error: any) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ error: 'VALIDATION_ERROR', details: error.errors });
      }
      res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi thêm mới sản phẩm' });
    }
  }
);

export default router;
