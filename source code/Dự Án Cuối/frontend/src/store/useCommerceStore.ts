import { create } from 'zustand';
import { Product, Category, Cart, Quote, Order, User, ChatMessage, ActionApproval } from '../types';
import { api, setAuthToken } from '../services/api';

// Demo fallback mock products if backend is not yet started or during quick load
const FALLBACK_PRODUCTS: Product[] = [
  {
    id: 1,
    sku: 'LAP-DELL-XPS13',
    name: 'Laptop Dell XPS 13 Plus 9320 (Core i7 / 16GB / 512GB SSD)',
    slug: 'laptop-dell-xps-13-plus-9320',
    description: 'Laptop doanh nhân siêu mỏng nhẹ, màn hình OLED 3.5K sắc nét, pin 12 tiếng, thiết kế nhôm nguyên khối sang trọng.',
    priceMinor: 32990000,
    stockQty: 15,
    categoryId: 1,
    category: { id: 1, name: 'Laptop & Máy tính', slug: 'laptops' },
    imageUrl: 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=600&auto=format&fit=crop&q=80',
    aiTags: ['mong-nhe', 'van-phong', 'do-hoa', 'pin-trau', 'cao-cap'],
    specs: { cpu: 'Intel Core i7-1360P', ram: '16GB LPDDR5', storage: '512GB NVMe SSD', display: '13.4 inch 3.5K OLED' },
    status: 'ACTIVE'
  },
  {
    id: 2,
    sku: 'LAP-MAC-M3-15',
    name: 'MacBook Air M3 15-inch (8-Core GPU / 16GB / 512GB)',
    slug: 'macbook-air-m3-15-inch',
    description: 'Trải nghiệm đỉnh cao với chip Apple M3, pin dùng đến 18 giờ liên tục, màn hình Liquid Retina tuyệt đẹp và thiết kế không quạt êm ái.',
    priceMinor: 37990000,
    stockQty: 8,
    categoryId: 1,
    category: { id: 1, name: 'Laptop & Máy tính', slug: 'laptops' },
    imageUrl: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80',
    aiTags: ['mong-nhe', 'pin-trau', 'hoc-tap', 'van-phong', 'apple'],
    specs: { chip: 'Apple M3 8-Core', ram: '16GB Unified', storage: '512GB SSD', display: '15.3 inch Liquid Retina' },
    status: 'ACTIVE'
  },
  {
    id: 3,
    sku: 'AUD-SONY-XM5',
    name: 'Tai nghe Sony WH-1000XM5 Chống Ồn Chủ Động Cao Cấp',
    slug: 'tai-nghe-sony-wh-1000xm5',
    description: 'Công nghệ chống ồn chủ động đỉnh cao số 1 thế giới, chất lượng âm thanh Hi-Res không dây, micro AI đàm thoại pha lê.',
    priceMinor: 7990000,
    stockQty: 25,
    categoryId: 2,
    category: { id: 2, name: 'Phụ kiện & Âm thanh', slug: 'accessories-audio' },
    imageUrl: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80',
    aiTags: ['chong-on', 'pin-trau', 'am-thanh-hifi', 'du-lich'],
    specs: { battery: '30 giờ (bật ANC)', driver: '30mm Carbon', noiseCancelling: 'Dual Processor V1 + QN1' },
    status: 'ACTIVE'
  },
  {
    id: 4,
    sku: 'ACC-KEYCHRON-Q1',
    name: 'Bàn phím cơ không dây Keychron Q1 Pro QMK/VIA Hot-swap',
    slug: 'ban-phim-co-keychron-q1-pro',
    description: 'Vỏ nhôm CNC cao cấp, kết nối Bluetooth 5.1 & dây Type-C, núm xoay đa năng tùy biến qua QMK/VIA.',
    priceMinor: 4290000,
    stockQty: 20,
    categoryId: 2,
    category: { id: 2, name: 'Phụ kiện & Âm thanh', slug: 'accessories-audio' },
    imageUrl: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80',
    aiTags: ['ban-phim-co', 'lap-trinh', 'gaming', 'custom'],
    specs: { layout: '75%', body: 'Nhôm CNC Anodized', switch: 'Keychron K Pro Brown' },
    status: 'ACTIVE'
  },
  {
    id: 5,
    sku: 'ACC-LOGI-MX3S',
    name: 'Chuột không dây Logitech MX Master 3S Ergonomic',
    slug: 'chuot-khong-day-logitech-mx-master-3s',
    description: 'Cảm biến 8.000 DPI di chuyển trên mọi bề mặt kể cả mặt kính. Con lăn điện từ MagSpeed cuộn 1.000 dòng/giây và click êm ái Quiet Clicks.',
    priceMinor: 2490000,
    stockQty: 40,
    categoryId: 2,
    category: { id: 2, name: 'Phụ kiện & Âm thanh', slug: 'accessories-audio' },
    imageUrl: 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600&auto=format&fit=crop&q=80',
    aiTags: ['van-phong', 'ergonomic', 'pin-trau', 'lap-trinh'],
    specs: { dpi: '8000 DPI', battery: '70 ngày', connection: 'Logi Bolt / Bluetooth' },
    status: 'ACTIVE'
  },
  {
    id: 6,
    sku: 'LIF-COFFEE-ARABICA',
    name: 'Cà phê Arabica Cầu Đất Thượng Hạng (Rang Mộc 500g)',
    slug: 'ca-phe-arabica-cau-dat-thuong-hang',
    description: '100% hạt cà phê Arabica Cầu Đất Đà Lạt tuyển chọn thủ công, thu hái chín cây ở độ cao 1.600m. Hương vị phong phú với nốt chua thanh tao và hậu ngọt dài lâu.',
    priceMinor: 280000,
    stockQty: 100,
    categoryId: 4,
    category: { id: 4, name: 'Đời sống & Tiện ích', slug: 'lifestyle' },
    imageUrl: 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=600&auto=format&fit=crop&q=80',
    aiTags: ['cafe', 'tinh-tao', 'huong-hoa-qua', 'thu-cong'],
    specs: { origin: 'Cầu Đất, Đà Lạt', roast: 'Medium Light', weight: '500g' },
    status: 'ACTIVE'
  },
  {
    id: 7,
    sku: 'LAP-HP-15S',
    name: 'Laptop HP 15s-fq5078TU (Core i3-1215U / 8GB / 256GB SSD)',
    slug: 'laptop-hp-15s-fq5078tu',
    description: 'Laptop học tập sinh viên giá mềm dưới 10 triệu, thiết kế mỏng nhẹ trang nhã, hiệu năng Intel Gen 12 mượt mà, màn hình lớn 15.6 inch.',
    priceMinor: 9990000,
    stockQty: 30,
    categoryId: 1,
    category: { id: 1, name: 'Laptop & Máy tính', slug: 'laptops' },
    imageUrl: 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=600&auto=format&fit=crop&q=80',
    aiTags: ['hoc-tap', 'sinh-vien', 'gia-re', 'van-phong', 'mong-nhe'],
    specs: { cpu: 'Intel Core i3-1215U', ram: '8GB DDR4', storage: '256GB SSD', display: '15.6 inch FHD' },
    status: 'ACTIVE'
  }
];

interface CommerceState {
  // Auth & Roles
  currentUser: User | null;
  currentRole: 'CUSTOMER' | 'ADMIN' | 'MERCHANT';
  
  // Catalog
  products: Product[];
  categories: Category[];
  selectedCategoryId: number | null;
  isLoadingProducts: boolean;
  
  // NLP Search
  nlpQuery: string;
  isNlpSearching: boolean;
  nlpIntent: any;
  
  // Cart & 15-min Frozen Quote
  cart: Cart | null;
  cartCount: number;
  activeQuote: Quote | null;
  quoteTimeRemaining: number; // seconds remaining
  quoteTimerId: any;
  
  // Orders
  orders: Order[];
  lastCreatedOrder: Order | null;
  
  // Modals & UI States
  isCartOpen: boolean;
  isCheckoutOpen: boolean;
  isAssistantOpen: boolean;
  isAdminOpen: boolean;
  selectedProduct: Product | null;
  
  // AI Assistant Chat & HITL
  chatMessages: ChatMessage[];
  isChatLoading: boolean;
  pendingApprovals: ActionApproval[];
  
  // Actions
  init: () => Promise<void>;
  switchRole: (role: 'CUSTOMER' | 'ADMIN' | 'MERCHANT') => Promise<void>;
  fetchProducts: (categoryId?: number, search?: string) => Promise<void>;
  executeNlpSearch: (query: string) => Promise<void>;
  resetCatalog: () => void;
  
  // Cart Actions
  addToCart: (productId: number, quantity?: number) => Promise<void>;
  updateCartItem: (itemId: number, quantity: number) => Promise<void>;
  removeCartItem: (itemId: number) => Promise<void>;
  createQuote: () => Promise<Quote | null>;
  
  // Checkout & Saga
  checkoutOrder: (payload: {
    shippingAddress: string;
    shippingPhone: string;
    recipientName: string;
    paymentMethod: 'VIETQR' | 'COD' | 'MOCK_GATEWAY';
  }) => Promise<{ success: boolean; order?: Order; error?: string }>;
  
  // AI Assistant & HITL
  sendChatMessage: (content: string) => Promise<void>;
  handleActionApproval: (action: ActionApproval, approved: boolean) => Promise<void>;
  
  // UI Triggers
  setSelectedProduct: (product: Product | null) => void;
  setCartOpen: (open: boolean) => void;
  setCheckoutOpen: (open: boolean) => void;
  setAssistantOpen: (open: boolean) => void;
  setAdminOpen: (open: boolean) => void;
  setLastCreatedOrder: (order: Order | null) => void;
}

export const useCommerceStore = create<CommerceState>((set, get) => ({
  currentUser: {
    id: 3,
    email: 'customer@gmail.com',
    fullName: 'Nguyễn Văn Khải (Customer)',
    phone: '0987654321',
    roleId: 3,
    role: { id: 3, name: 'CUSTOMER' }
  },
  currentRole: 'CUSTOMER',
  
  products: FALLBACK_PRODUCTS,
  categories: [
    { id: 1, name: 'Laptop & Máy tính', slug: 'laptops' },
    { id: 2, name: 'Phụ kiện & Âm thanh', slug: 'accessories-audio' },
    { id: 3, name: 'Điện thoại & Tablet', slug: 'phones-tablets' },
    { id: 4, name: 'Đời sống & Tiện ích', slug: 'lifestyle' }
  ],
  selectedCategoryId: null,
  isLoadingProducts: false,
  
  nlpQuery: '',
  isNlpSearching: false,
  nlpIntent: null,
  
  cart: null,
  cartCount: 0,
  activeQuote: null,
  quoteTimeRemaining: 0,
  quoteTimerId: null,
  
  orders: [],
  lastCreatedOrder: null,
  
  isCartOpen: false,
  isCheckoutOpen: false,
  isAssistantOpen: false,
  isAdminOpen: false,
  selectedProduct: null,
  
  chatMessages: [
    {
      id: 'welcome',
      role: 'assistant',
      content: '👋 Xin chào! Tôi là **Trợ lý Mua sắm Trí tuệ Nhân tạo** (AI-Native Shopping Agent).\n\nTôi có thể giúp bạn:\n• 🔍 Tìm kiếm sản phẩm theo ngôn ngữ tự nhiên (ví dụ: *"tìm laptop mỏng nhẹ dưới 35 triệu"*)\n• 🛒 Tự động tư vấn và thêm sản phẩm vào giỏ hàng an toàn\n• 📦 Tra cứu hành trình đơn hàng và chính sách bảo hành, hoàn trả\n\nBạn đang quan tâm đến sản phẩm nào?',
      timestamp: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
      suggestedActions: [
        'Laptop mỏng nhẹ dưới 35 triệu',
        'Tai nghe chống ồn cao cấp',
        'Chính sách đổi trả trong 7 ngày'
      ]
    }
  ],
  isChatLoading: false,
  pendingApprovals: [],

  init: async () => {
    // 1. Authenticate default customer demo account
    try {
      const loginRes = await api.auth.login('customer@gmail.com', 'Admin@123');
      setAuthToken(loginRes.token);
      set({ currentUser: loginRes.user });
      
      // Load cart
      const cartData = await api.cart.get().catch(() => null);
      if (cartData) {
        const count = cartData.items.reduce((sum, item) => sum + item.quantity, 0);
        set({ cart: cartData, cartCount: count });
      }
      
      // Load categories & products
      const cats = await api.catalog.getCategories().catch(() => null);
      if (cats && cats.length > 0) set({ categories: cats });
      
      const prodsRes = await api.catalog.getProducts().catch(() => null);
      if (prodsRes && prodsRes.products.length > 0) set({ products: prodsRes.products });
    } catch {
      // Offline fallback: keep fallback mock data
      console.log('Backend not reachable yet, using offline mock database');
    }
  },

  switchRole: async (role: 'CUSTOMER' | 'ADMIN' | 'MERCHANT') => {
    set({ currentRole: role });
    const email = role === 'ADMIN' ? 'admin@ainative.vn' : role === 'MERCHANT' ? 'merchant@ainative.vn' : 'customer@gmail.com';
    try {
      const loginRes = await api.auth.login(email, 'Admin@123');
      setAuthToken(loginRes.token);
      set({ currentUser: loginRes.user });
      if (role === 'ADMIN') {
        set({ isAdminOpen: true });
      }
    } catch (e) {
      console.error('Role switch failed:', e);
    }
  },

  fetchProducts: async (categoryId?: number, search?: string) => {
    set({ isLoadingProducts: true, selectedCategoryId: categoryId || null });
    try {
      const res = await api.catalog.getProducts({ categoryId, search });
      set({ products: res.products, isLoadingProducts: false });
    } catch {
      let filtered = [...FALLBACK_PRODUCTS];
      if (categoryId) filtered = filtered.filter(p => p.categoryId === categoryId);
      if (search) filtered = filtered.filter(p => p.name.toLowerCase().includes(search.toLowerCase()));
      set({ products: filtered, isLoadingProducts: false });
    }
  },

  executeNlpSearch: async (query: string) => {
    if (!query.trim()) {
      get().resetCatalog();
      return;
    }
    set({ isNlpSearching: true, nlpQuery: query });
    try {
      const res = await api.ai.nlpSearch(query);
      set({
        products: res.results,
        nlpIntent: res.detectedIntent,
        isNlpSearching: false
      });
    } catch {
      // Mock client NLP filter
      const q = query.toLowerCase();
      let maxBudget: number | null = null;
      const budgetMatch = q.match(/(?:dưới|tôi có|khoảng|tầm|ngân sách|<=?)\s*(\d+)\s*(triệu|tr|k)?/i) || q.match(/(\d+)\s*(triệu|tr)/i);
      if (budgetMatch) {
        const num = parseFloat(budgetMatch[1]);
        const unit = budgetMatch[2]?.toLowerCase();
        if (unit === 'k') maxBudget = num * 1000;
        else maxBudget = num * 1000000;
      }

      const scored = FALLBACK_PRODUCTS.map(p => {
        let score = 0;
        const corpus = `${p.name} ${p.description} ${p.aiTags?.join(' ')} ${p.category.name}`.toLowerCase();
        
        if (q.includes('laptop') && p.categoryId === 1) score += 6;
        if (q.includes('tai nghe') && p.categoryId === 2) score += 6;
        if (q.includes('mỏng nhẹ') && corpus.includes('mong-nhe')) score += 4;
        if (q.includes('sinh viên') || q.includes('học tập')) {
          if (corpus.includes('hoc-tap') || corpus.includes('sinh-vien')) score += 5;
        }

        if (maxBudget) {
          if (p.priceMinor <= maxBudget) score += 8;
          else score -= 15; // heavy penalty for exceeding budget
        }

        return { product: p, score };
      })
      .filter(x => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .map(x => ({
        ...x.product,
        matchScore: x.score,
        aiExplanation: `Phù hợp với nhu cầu '${query}'`
      }));

      set({
        products: scored,
        isNlpSearching: false,
        nlpIntent: { query, maxPriceMinor: maxBudget, count: scored.length }
      });
    }
  },

  resetCatalog: () => {
    set({ nlpQuery: '', nlpIntent: null, selectedCategoryId: null, products: FALLBACK_PRODUCTS });
  },

  addToCart: async (productId: number, quantity: number = 1) => {
    try {
      const cart = await api.cart.addItem(productId, quantity);
      const count = cart.items.reduce((sum, item) => sum + item.quantity, 0);
      set({ cart, cartCount: count, activeQuote: null }); // Invalidate quote upon cart change
    } catch {
      // Fallback local cart state
      const existing = get().cart?.items || [];
      const prod = FALLBACK_PRODUCTS.find(p => p.id === productId);
      if (!prod) return;

      const foundIdx = existing.findIndex(i => i.productId === productId);
      let newItems = [...existing];
      if (foundIdx >= 0) {
        newItems[foundIdx].quantity += quantity;
      } else {
        newItems.push({
          id: Date.now(),
          productId: prod.id,
          product: prod,
          quantity,
          unitPriceMinor: prod.priceMinor
        });
      }
      const subtotal = newItems.reduce((sum, i) => sum + i.quantity * i.unitPriceMinor, 0);
      const totalCount = newItems.reduce((sum, i) => sum + i.quantity, 0);
      set({
        cart: { id: 1, userId: 3, items: newItems, subtotalMinor: subtotal },
        cartCount: totalCount,
        activeQuote: null
      });
    }
  },

  updateCartItem: async (itemId: number, quantity: number) => {
    try {
      const cart = await api.cart.updateItem(itemId, quantity);
      const count = cart.items.reduce((sum, item) => sum + item.quantity, 0);
      set({ cart, cartCount: count, activeQuote: null });
    } catch {
      const items = (get().cart?.items || []).map(i => i.id === itemId ? { ...i, quantity } : i);
      const subtotal = items.reduce((sum, i) => sum + i.quantity * i.unitPriceMinor, 0);
      const totalCount = items.reduce((sum, i) => sum + i.quantity, 0);
      set({ cart: { id: 1, userId: 3, items, subtotalMinor: subtotal }, cartCount: totalCount, activeQuote: null });
    }
  },

  removeCartItem: async (itemId: number) => {
    try {
      const res = await api.cart.removeItem(itemId);
      const count = res.cart.items.reduce((sum, item) => sum + item.quantity, 0);
      set({ cart: res.cart, cartCount: count, activeQuote: null });
    } catch {
      const items = (get().cart?.items || []).filter(i => i.id !== itemId);
      const subtotal = items.reduce((sum, i) => sum + i.quantity * i.unitPriceMinor, 0);
      const totalCount = items.reduce((sum, i) => sum + i.quantity, 0);
      set({ cart: { id: 1, userId: 3, items, subtotalMinor: subtotal }, cartCount: totalCount, activeQuote: null });
    }
  },

  createQuote: async () => {
    // Clear previous timer
    if (get().quoteTimerId) clearInterval(get().quoteTimerId);

    try {
      const res = await api.cart.createQuote();
      const quote = res.quote;
      const remainingSeconds = 15 * 60; // 15 minutes

      const timerId = setInterval(() => {
        const cur = get().quoteTimeRemaining;
        if (cur <= 1) {
          clearInterval(get().quoteTimerId);
          set({ activeQuote: null, quoteTimeRemaining: 0 });
        } else {
          set({ quoteTimeRemaining: cur - 1 });
        }
      }, 1000);

      set({ activeQuote: quote, quoteTimeRemaining: remainingSeconds, quoteTimerId: timerId });
      return quote;
    } catch {
      // Local quote fallback
      const cart = get().cart;
      if (!cart || cart.items.length === 0) return null;
      const subtotal = cart.subtotalMinor;
      const discount = subtotal > 30000000 ? 500000 : 0;
      const shipping = subtotal > 2000000 ? 0 : 30000;
      const tax = Math.round((subtotal - discount) * 0.1);
      const total = subtotal - discount + shipping + tax;

      const mockQuote: Quote = {
        id: `QT-${Date.now()}`,
        cartId: cart.id,
        subtotalMinor: subtotal,
        discountMinor: discount,
        shippingMinor: shipping,
        taxMinor: tax,
        totalMinor: total,
        currency: 'VND',
        fingerprint: `fp_sha256_${Math.random().toString(36).substring(2, 18)}`,
        expiresAt: new Date(Date.now() + 15 * 60 * 1000).toISOString(),
        items: cart.items.map(i => ({
          productId: i.productId,
          name: i.product.name,
          quantity: i.quantity,
          priceMinor: i.unitPriceMinor,
          lineTotalMinor: i.quantity * i.unitPriceMinor
        }))
      };

      const timerId = setInterval(() => {
        const cur = get().quoteTimeRemaining;
        if (cur <= 1) {
          clearInterval(get().quoteTimerId);
          set({ activeQuote: null, quoteTimeRemaining: 0 });
        } else {
          set({ quoteTimeRemaining: cur - 1 });
        }
      }, 1000);

      set({ activeQuote: mockQuote, quoteTimeRemaining: 15 * 60, quoteTimerId: timerId });
      return mockQuote;
    }
  },

  checkoutOrder: async (payload) => {
    const quote = get().activeQuote;
    if (!quote) return { success: false, error: 'Chưa có báo giá đóng băng hợp lệ. Vui lòng tạo báo giá.' };

    try {
      const res = await api.checkout.process({
        quoteId: quote.id,
        shippingAddress: payload.shippingAddress,
        shippingPhone: payload.shippingPhone,
        recipientName: payload.recipientName,
        paymentMethod: payload.paymentMethod
      });

      // Clear cart & quote
      if (get().quoteTimerId) clearInterval(get().quoteTimerId);
      set({
        cart: null,
        cartCount: 0,
        activeQuote: null,
        quoteTimeRemaining: 0,
        lastCreatedOrder: res.order,
        isCheckoutOpen: false,
        isCartOpen: false
      });

      return { success: true, order: res.order };
    } catch (err: any) {
      // Local demo fallback order
      const fallbackOrder: Order = {
        id: Date.now(),
        orderNumber: `ORD-${Date.now().toString().slice(-6)}`,
        userId: 3,
        status: payload.paymentMethod === 'VIETQR' ? 'CONFIRMED' : 'PENDING_PAYMENT',
        totalMinor: quote.totalMinor,
        currency: 'VND',
        shippingAddress: payload.shippingAddress,
        shippingPhone: payload.shippingPhone,
        recipientName: payload.recipientName,
        paymentMethod: payload.paymentMethod,
        paymentStatus: payload.paymentMethod === 'VIETQR' ? 'PAID' : 'PENDING',
        createdAt: new Date().toISOString(),
        items: quote.items.map((i, idx) => ({
          id: idx + 1,
          productId: i.productId,
          product: FALLBACK_PRODUCTS.find(p => p.id === i.productId) || FALLBACK_PRODUCTS[0],
          quantity: i.quantity,
          unitPriceMinor: i.priceMinor,
          subtotalMinor: i.lineTotalMinor
        }))
      };

      if (get().quoteTimerId) clearInterval(get().quoteTimerId);
      set({
        cart: null,
        cartCount: 0,
        activeQuote: null,
        quoteTimeRemaining: 0,
        lastCreatedOrder: fallbackOrder,
        isCheckoutOpen: false,
        isCartOpen: false
      });

      return { success: true, order: fallbackOrder };
    }
  },

  sendChatMessage: async (content: string) => {
    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
    };

    set(state => ({
      chatMessages: [...state.chatMessages, userMsg],
      isChatLoading: true
    }));

    try {
      const history = get().chatMessages.map(m => ({ role: m.role, content: m.content }));
      const res = await api.ai.chatAssistant({ message: content, history });

      const assistantMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: res.reply,
        timestamp: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
        intent: res.intent,
        suggestedProducts: res.suggestedProducts,
        suggestedActions: res.suggestedActions,
        proposedAction: res.proposedAction
      };

      set(state => ({
        chatMessages: [...state.chatMessages, assistantMsg],
        isChatLoading: false
      }));
    } catch {
      // Offline fallback agent response
      let reply = `Tôi đã nhận được yêu cầu: "${content}".`;
      let proposedAction: ActionApproval | undefined;
      const lower = content.toLowerCase();

      if (lower.includes('laptop') || lower.includes('35 triệu')) {
        reply = 'Dựa trên nhu cầu mỏng nhẹ và ngân sách dưới 35 triệu, tôi đề xuất **Dell XPS 13 Plus 9320** (32.990.000 đ) với chip Core i7 và màn hình OLED 3.5K sắc nét.';
        proposedAction = {
          actionType: 'ADD_TO_CART',
          description: 'Thêm Laptop Dell XPS 13 Plus 9320 (SL: 1) vào giỏ hàng',
          payload: { productId: 1, quantity: 1 },
          requiresConfirmation: true,
          status: 'PENDING'
        };
      } else if (lower.includes('tai nghe') || lower.includes('chống ồn')) {
        reply = 'Chiếc **Sony WH-1000XM5** (7.990.000 đ) là tai nghe chống ồn chủ động tốt nhất hiện nay, pin 30 giờ và hỗ trợ đàm thoại AI lọc tạp âm rất thích hợp cho làm việc.';
        proposedAction = {
          actionType: 'ADD_TO_CART',
          description: 'Thêm Tai nghe Sony WH-1000XM5 (SL: 1) vào giỏ hàng',
          payload: { productId: 3, quantity: 1 },
          requiresConfirmation: true,
          status: 'PENDING'
        };
      } else if (lower.includes('đổi trả') || lower.includes('bảo hành')) {
        reply = 'Chính sách hoàn trả của AI-Native Commerce áp dụng trong vòng **7 ngày** kể từ ngày giao hàng thành công. Sản phẩm cần còn nguyên tem và phụ kiện. AI Return Agent sẽ hỗ trợ tạo mã vận đơn hoàn trả tự động nếu đạt điều kiện.';
      }

      const assistantMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: reply,
        timestamp: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
        proposedAction
      };

      set(state => ({
        chatMessages: [...state.chatMessages, assistantMsg],
        isChatLoading: false
      }));
    }
  },

  handleActionApproval: async (action: ActionApproval, approved: boolean) => {
    if (!approved) {
      set(state => ({
        chatMessages: [
          ...state.chatMessages,
          {
            id: `sys-${Date.now()}`,
            role: 'system',
            content: `🚫 Bạn đã từ chối thao tác: "${action.description}". Thao tác đã bị hủy bỏ an toàn.`,
            timestamp: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
          }
        ]
      }));
      return;
    }

    // Execute approved action
    if (action.actionType === 'ADD_TO_CART') {
      const { productId, quantity } = action.payload;
      await get().addToCart(productId, quantity || 1);
      set(state => ({
        chatMessages: [
          ...state.chatMessages,
          {
            id: `sys-${Date.now()}`,
            role: 'system',
            content: `✅ Phê duyệt thành công! Đã thêm sản phẩm vào giỏ hàng cá nhân. Bạn có thể mở Giỏ hàng để xem báo giá đóng băng 15 phút.`,
            timestamp: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
          }
        ]
      }));
    }
  },

  setSelectedProduct: (product) => set({ selectedProduct: product }),
  setCartOpen: (open) => set({ isCartOpen: open }),
  setCheckoutOpen: (open) => set({ isCheckoutOpen: open }),
  setAssistantOpen: (open) => set({ isAssistantOpen: open }),
  setAdminOpen: (open) => set({ isAdminOpen: open }),
  setLastCreatedOrder: (order) => set({ lastCreatedOrder: order })
}));
