import express, { Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

import authRouter from './routes/auth';
import catalogRouter from './routes/catalog';
import cartRouter from './routes/cart';
import checkoutRouter from './routes/checkout';
import ordersRouter from './routes/orders';
import aiRouter from './routes/ai';
import adminRouter from './routes/admin';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors({ origin: '*' }));
app.use(express.json());

// Health Check
app.get('/health', (_req: Request, res: Response) => {
  res.json({
    status: 'ok',
    service: 'AI-Native Commerce Backend API',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// API Routes
app.use('/api/v1/auth', authRouter);
app.use('/api/v1/catalog', catalogRouter);
app.use('/api/v1/carts', cartRouter);
app.use('/api/v1/checkout', checkoutRouter);
app.use('/api/v1/orders', ordersRouter);
app.use('/api/v1/ai', aiRouter);
app.use('/api/v1/admin', adminRouter);

app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`🚀 AI-Native Commerce Backend API is running!`);
  console.log(`📡 URL: http://localhost:${PORT}`);
  console.log(`🏥 Health Check: http://localhost:${PORT}/health`);
  console.log(`📚 OpenAPI Spec: docs/02-ky-thuat/openapi.yaml`);
  console.log(`=======================================================`);
});
