import { Request, Response, NextFunction } from 'express';
import crypto from 'crypto';
import prisma from '../lib/prisma';

export const handleIdempotency = (operationName: string) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const idempotencyKey = req.headers['idempotency-key'] as string;
    if (!idempotencyKey || !req.user) {
      return next(); // Skip if no key provided or unauthenticated
    }

    const actorId = req.user.id;
    const bodyStr = JSON.stringify(req.body || {});
    const requestHash = crypto.createHash('sha256').update(bodyStr).digest('hex');

    try {
      const existing = await prisma.idempotencyRecord.findUnique({
        where: {
          actorId_operation_requestKey: {
            actorId,
            operation: operationName,
            requestKey: idempotencyKey
          }
        }
      });

      if (existing) {
        if (existing.status === 'COMPLETED' && existing.responseJson && existing.httpStatus) {
          return res.status(existing.httpStatus).json(JSON.parse(existing.responseJson));
        }
        if (existing.status === 'PENDING') {
          return res.status(409).json({
            error: 'CONFLICT',
            message: 'Yêu cầu đang được xử lý song song, vui lòng đợi.'
          });
        }
      }

      // Record pending execution
      const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000); // 24 hours
      await prisma.idempotencyRecord.create({
        data: {
          actorId,
          operation: operationName,
          requestKey: idempotencyKey,
          requestHash,
          status: 'PENDING',
          expiresAt
        }
      });

      // Intercept res.json to capture response
      const originalJson = res.json.bind(res);
      res.json = (body: any) => {
        prisma.idempotencyRecord.update({
          where: {
            actorId_operation_requestKey: {
              actorId,
              operation: operationName,
              requestKey: idempotencyKey
            }
          },
          data: {
            status: 'COMPLETED',
            httpStatus: res.statusCode,
            responseJson: JSON.stringify(body)
          }
        }).catch(err => console.error('Failed to update idempotency record:', err));

        return originalJson(body);
      };

      next();
    } catch (error) {
      console.error('Idempotency middleware error:', error);
      next();
    }
  };
};
