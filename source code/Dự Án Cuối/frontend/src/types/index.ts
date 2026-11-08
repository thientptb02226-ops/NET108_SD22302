export interface Role {
  id: number;
  name: 'ADMIN' | 'MERCHANT' | 'CUSTOMER';
  description?: string;
}

export interface User {
  id: number;
  email: string;
  fullName: string;
  phone?: string;
  roleId: number;
  role: Role;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  icon?: string;
  description?: string;
}

export interface Product {
  id: number;
  sku: string;
  name: string;
  slug: string;
  description?: string;
  priceMinor: number;
  stockQty: number;
  categoryId: number;
  category: Category;
  imageUrl?: string;
  specs?: Record<string, any>;
  aiTags?: string[];
  status: string;
  matchScore?: number;
  aiExplanation?: string;
}

export interface CartItem {
  id: number;
  productId: number;
  product: Product;
  quantity: number;
  unitPriceMinor: number;
}

export interface Cart {
  id: number;
  userId: number;
  items: CartItem[];
  subtotalMinor: number;
}

export interface Quote {
  id: string;
  cartId: number;
  subtotalMinor: number;
  discountMinor: number;
  shippingMinor: number;
  taxMinor: number;
  totalMinor: number;
  currency: string;
  fingerprint: string;
  expiresAt: string;
  items: Array<{
    productId: number;
    name: string;
    quantity: number;
    priceMinor: number;
    lineTotalMinor: number;
  }>;
}

export interface OrderItem {
  id: number;
  productId: number;
  product: Product;
  quantity: number;
  unitPriceMinor: number;
  subtotalMinor: number;
}

export interface Order {
  id: number;
  orderNumber: string;
  userId: number;
  status: 'PENDING_PAYMENT' | 'CONFIRMED' | 'PROCESSING' | 'SHIPPED' | 'DELIVERED' | 'COMPLETED' | 'CANCELLED';
  totalMinor: number;
  currency: string;
  shippingAddress: string;
  shippingPhone: string;
  recipientName: string;
  paymentMethod: string;
  paymentStatus: string;
  createdAt: string;
  items: OrderItem[];
}

export interface ActionApproval {
  actionType: 'ADD_TO_CART' | 'APPLY_VOUCHER' | 'CHECK_ORDER' | 'REQUEST_RETURN';
  description: string;
  payload: Record<string, any>;
  requiresConfirmation: boolean;
  status?: 'PENDING' | 'APPROVED' | 'REJECTED';
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  intent?: string;
  suggestedProducts?: Product[];
  suggestedActions?: string[];
  proposedAction?: ActionApproval;
}
