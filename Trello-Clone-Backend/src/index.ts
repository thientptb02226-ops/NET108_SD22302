import express, { Request, Response } from 'express';
import cors from 'cors';
import { createServer } from 'http';
import { Server } from 'socket.io';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const server = createServer(app);
const io = new Server(server, {
  cors: { origin: '*' }
});

const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Health Check
app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok', service: 'Trello-Clone-Backend', timestamp: new Date() });
});

// API Routes prefix
app.get('/api/v1/boards', (_req: Request, res: Response) => {
  res.json([
    {
      id: 'board-1',
      title: 'Sprint Backlog',
      lists: [
        { id: 'list-1', title: 'To Do', cards: [{ id: 'card-1', title: 'Setup Multi-Agent Architecture' }] },
        { id: 'list-2', title: 'In Progress', cards: [] },
        { id: 'list-3', title: 'Done', cards: [] }
      ]
    }
  ]);
});

// Real-time card movement socket
io.on('connection', (socket) => {
  console.log(`[Socket] Client connected: ${socket.id}`);

  socket.on('join_board', (boardId: string) => {
    socket.join(boardId);
    console.log(`[Socket] Client ${socket.id} joined board: ${boardId}`);
  });

  socket.on('card_moved', (data) => {
    socket.to(data.boardId).emit('card_updated', data);
  });

  socket.on('disconnect', () => {
    console.log(`[Socket] Client disconnected: ${socket.id}`);
  });
});

server.listen(PORT, () => {
  console.log(`🚀 Trello Clone Backend running on http://localhost:${PORT}`);
});

