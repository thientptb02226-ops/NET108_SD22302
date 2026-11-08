import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET || 'ai-native-commerce-super-secret-key-2026';

export interface AuthUser {
  id: number;
  email: string;
  roleName: string;
  fullName: string;
}

declare global {
  namespace Express {
    interface Request {
      user?: AuthUser;
    }
  }
}

export const authenticateToken = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({
      error: 'UNAUTHENTICATED',
      message: 'Token xác thực không tồn tại hoặc đã hết hạn'
    });
  }

  jwt.verify(token, JWT_SECRET, (err, decoded) => {
    if (err) {
      return res.status(403).json({
        error: 'FORBIDDEN',
        message: 'Token xác thực không hợp lệ'
      });
    }
    req.user = decoded as AuthUser;
    next();
  });
};

export const requireRole = (...allowedRoles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'UNAUTHENTICATED', message: 'Yêu cầu đăng nhập' });
    }

    if (!allowedRoles.includes(req.user.roleName)) {
      return res.status(403).json({
        error: 'PERMISSION_DENIED',
        message: `Tài khoản với vai trò '${req.user.roleName}' không có quyền truy cập chức năng này`
      });
    }

    next();
  };
};
