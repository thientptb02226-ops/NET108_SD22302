# API Specifications

Base URL: `http://localhost:5000/api/v1`

## Data Models

```typescript
export interface User {
  id: string;
  email: string;
  name: string;
  avatarUrl?: string;
  createdAt: string;
}

export interface Board {
  id: string;
  title: string;
  description?: string;
  background?: string;
  ownerId: string;
  lists?: List[];
  createdAt: string;
}

export interface List {
  id: string;
  boardId: string;
  title: string;
  position: number;
  cards?: Card[];
}

export interface Card {
  id: string;
  listId: string;
  title: string;
  description?: string;
  position: number;
  dueDate?: string;
  labels?: string[];
  commentsCount?: number;
}
```

