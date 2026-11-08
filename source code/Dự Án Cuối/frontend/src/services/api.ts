import { Product, Category, Cart, Quote, Order, ChatMessage, ActionApproval } from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api/v1';

// In-memory token storage
let authToken: string = localStorage.getItem('ainative_token') || '';

export const setAuthToken = (token: string) => {
  authToken = token;
  if (token) {
    localStorage.setItem('ainative_token', token);
  } else {
    localStorage.removeItem('ainative_token');
  }
};

export const getAuthToken = () => authToken;

// Helper fetch with headers
async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.message || `API Error: ${res.statusText} (${res.status})`);
  }

  return res.json();
}

// -------------------------------------------------------------
// API Services
// -------------------------------------------------------------

export const api = {
  // Auth
  auth: {
    login: (email: string, password: string) =>
      request<{ token: string; user: any }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }),
    me: () => request<{ user: any }>('/auth/me'),
  },

  // Catalog
  catalog: {
    getCategories: () => request<Category[]>('/catalog/categories'),
    getProducts: (params?: { categoryId?: number; search?: string; page?: number; limit?: number }) => {
      const query = new URLSearchParams();
      if (params?.categoryId) query.append('categoryId', params.categoryId.toString());
      if (params?.search) query.append('search', params.search);
      if (params?.page) query.append('page', params.page.toString());
      if (params?.limit) query.append('limit', params.limit.toString());
      return request<{ products: Product[]; pagination: any }>(`/catalog/products?${query.toString()}`);
    },
    getProductBySlug: (slug: string) => request<Product>(`/catalog/products/${slug}`),
  },

  // Cart
  cart: {
    get: () => request<Cart>('/cart'),
    addItem: (productId: number, quantity: number = 1) =>
      request<Cart>('/cart/items', {
        method: 'POST',
        body: JSON.stringify({ productId, quantity }),
      }),
    updateItem: (itemId: number, quantity: number) =>
      request<Cart>(`/cart/items/${itemId}`, {
        method: 'PUT',
        body: JSON.stringify({ quantity }),
      }),
    removeItem: (itemId: number) =>
      request<{ message: string; cart: Cart }>(`/cart/items/${itemId}`, {
        method: 'DELETE',
      }),
    createQuote: () =>
      request<{ quote: Quote; message: string }>('/cart/quote', {
        method: 'POST',
      }),
  },

  // Checkout (Saga with Idempotency)
  checkout: {
    process: (data: {
      quoteId: string;
      shippingAddress: string;
      shippingPhone: string;
      recipientName: string;
      paymentMethod: 'VIETQR' | 'COD' | 'MOCK_GATEWAY';
      idempotencyKey?: string;
    }) => {
      const key = data.idempotencyKey || `idem-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
      return request<{
        order: Order;
        payment: { paymentMethod: string; paymentStatus: string; qrCodeUrl?: string };
        message: string;
      }>('/checkout', {
        method: 'POST',
        headers: {
          'Idempotency-Key': key,
        },
        body: JSON.stringify({
          quoteId: data.quoteId,
          shippingAddress: data.shippingAddress,
          shippingPhone: data.shippingPhone,
          recipientName: data.recipientName,
          paymentMethod: data.paymentMethod,
        }),
      });
    },
  },

  // Orders
  orders: {
    getAll: () => request<Order[]>('/orders'),
    getById: (id: number) => request<Order>(`/orders/${id}`),
    cancel: (id: number, reason: string) =>
      request<{ message: string; order: Order }>(`/orders/${id}/cancel`, {
        method: 'POST',
        body: JSON.stringify({ reason }),
      }),
  },

  // AI & NLP Services
  ai: {
    nlpSearch: (query: string) =>
      request<{
        query: string;
        detectedIntent: any;
        matchCount: number;
        results: Product[];
      }>('/ai/nlp-search', {
        method: 'POST',
        body: JSON.stringify({ query }),
      }),
    chatAssistant: (data: {
      message: string;
      sessionId?: string;
      history?: Array<{ role: string; content: string }>;
    }) =>
      request<{
        sessionId: string;
        reply: string;
        intent: string;
        suggestedProducts?: Product[];
        suggestedActions?: string[];
        proposedAction?: ActionApproval;
      }>('/ai/assistant/chat', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    approveAction: (actionId: number, approved: boolean) =>
      request<{ message: string; status: string; result?: any }>('/ai/assistant/approve', {
        method: 'POST',
        body: JSON.stringify({ actionId, approved }),
      }),
  },

  // Admin Portal
  admin: {
    getStats: () =>
      request<{
        totalRevenueMinor: number;
        totalOrders: number;
        totalCustomers: number;
        totalProducts: number;
        recentOrders: Order[];
        revenueByDay: Array<{ day: string; revenue: number }>;
      }>('/admin/dashboard'),
    updateOrderStatus: (orderId: number, status: string) =>
      request<{ message: string; order: Order }>(`/admin/orders/${orderId}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status }),
      }),
  },
};
