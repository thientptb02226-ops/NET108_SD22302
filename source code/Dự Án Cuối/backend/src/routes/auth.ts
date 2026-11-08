import { Router, Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { z } from 'zod';
import prisma from '../lib/prisma';
import { authenticateToken } from '../middleware/auth';

const router = Router();
const JWT_SECRET = process.env.JWT_SECRET || 'ai-native-commerce-super-secret-key-2026';

const registerSchema = z.object({
  email: z.string().email('Email không đúng định dạng'),
  password: z.string().min(6, 'Mật khẩu phải từ 6 ký tự trở lên'),
  fullName: z.string().min(2, 'Họ và tên tối thiểu 2 ký tự'),
  phone: z.string().optional()
});

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1)
});

// POST /api/v1/auth/register
router.post('/register', async (req: Request, res: Response) => {
  try {
    const data = registerSchema.parse(req.body);

    const existingUser = await prisma.user.findUnique({
      where: { email: data.email }
    });

    if (existingUser) {
      return res.status(400).json({ error: 'EMAIL_EXISTS', message: 'Email này đã được đăng ký trên hệ thống' });
    }

    const salt = await bcrypt.genSalt(10);
    const passwordHash = await bcrypt.hash(data.password, salt);

    const defaultRole = await prisma.role.findFirst({ where: { name: 'Customer' } });

    const newUser = await prisma.user.create({
      data: {
        email: data.email,
        passwordHash,
        fullName: data.fullName,
        phone: data.phone,
        roleId: defaultRole ? defaultRole.id : 3
      },
      include: { role: true }
    });

    const token = jwt.sign(
      {
        id: newUser.id,
        email: newUser.email,
        fullName: newUser.fullName,
        roleName: newUser.role.name
      },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    res.status(201).json({
      message: 'Đăng ký tài khoản thành công',
      token,
      user: {
        id: newUser.id,
        email: newUser.email,
        fullName: newUser.fullName,
        role: newUser.role.name
      }
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: 'VALIDATION_ERROR', details: error.errors });
    }
    console.error('Register error:', error);
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi máy chủ khi đăng ký tài khoản' });
  }
});

// POST /api/v1/auth/login
router.post('/login', async (req: Request, res: Response) => {
  try {
    const { email, password } = loginSchema.parse(req.body);

    const user = await prisma.user.findUnique({
      where: { email },
      include: { role: true }
    });

    if (!user) {
      return res.status(401).json({ error: 'INVALID_CREDENTIALS', message: 'Email hoặc mật khẩu không chính xác' });
    }

    if (user.status !== 'ACTIVE') {
      return res.status(403).json({ error: 'ACCOUNT_LOCKED', message: 'Tài khoản của bạn đã bị khóa hoặc tạm ngưng' });
    }

    const isMatch = await bcrypt.compare(password, user.passwordHash);
    if (!isMatch) {
      return res.status(401).json({ error: 'INVALID_CREDENTIALS', message: 'Email hoặc mật khẩu không chính xác' });
    }

    const token = jwt.sign(
      {
        id: user.id,
        email: user.email,
        fullName: user.fullName,
        roleName: user.role.name
      },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    res.json({
      message: 'Đăng nhập thành công',
      token,
      user: {
        id: user.id,
        email: user.email,
        fullName: user.fullName,
        role: user.role.name
      }
    });
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: 'VALIDATION_ERROR', details: error.errors });
    }
    console.error('Login error:', error);
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi máy chủ khi đăng nhập' });
  }
});

// GET /api/v1/auth/me
router.get('/me', authenticateToken, async (req: Request, res: Response) => {
  try {
    const user = await prisma.user.findUnique({
      where: { id: req.user!.id },
      include: { role: true }
    });

    if (!user) {
      return res.status(404).json({ error: 'NOT_FOUND', message: 'Không tìm thấy thông tin người dùng' });
    }

    res.json({
      user: {
        id: user.id,
        email: user.email,
        fullName: user.fullName,
        phone: user.phone,
        avatarUrl: user.avatarUrl,
        role: user.role.name,
        status: user.status,
        createdAt: user.createdAt
      }
    });
  } catch (error) {
    res.status(500).json({ error: 'INTERNAL_ERROR', message: 'Lỗi máy chủ khi lấy thông tin cá nhân' });
  }
});

export default router;
