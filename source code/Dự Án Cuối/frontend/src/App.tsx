import React, { useEffect } from 'react';
import { 
  Sparkles, 
  RotateCcw, 
  Layers, 
  SlidersHorizontal,
  Bot,
  ShieldCheck,
  CheckCircle2,
  PackageCheck
} from 'lucide-react';
import { Navbar } from './components/Navbar';
import { HeroBanner } from './components/HeroBanner';
import { ProductCard } from './components/ProductCard';
import { ProductModal } from './components/ProductModal';
import { CartDrawer } from './components/CartDrawer';
import { CheckoutModal } from './components/CheckoutModal';
import { OrderSuccessModal } from './components/OrderSuccessModal';
import { AiAssistantWidget } from './components/AiAssistantWidget';
import { AdminDashboard } from './components/AdminDashboard';
import { useCommerceStore } from './store/useCommerceStore';

export const App: React.FC = () => {
  const {
    init,
    products,
    categories,
    selectedCategoryId,
    fetchProducts,
    nlpQuery,
    nlpIntent,
    resetCatalog,
    isLoadingProducts
  } = useCommerceStore();

  useEffect(() => {
    init();
  }, [init]);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 selection:bg-indigo-600 selection:text-white">
      
      {/* 1. Header Navigation */}
      <Navbar />

      {/* 2. Hero Architectural Banner */}
      <HeroBanner />

      {/* 3. Main Catalog Section */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
        
        {/* NLP Active Filter Notification Banner (if searching) */}
        {nlpQuery && (
          <div className="p-4 rounded-2xl bg-indigo-50 border border-indigo-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 animate-in fade-in">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-indigo-600 text-white flex items-center justify-center shrink-0">
                <Sparkles className="w-5 h-5 text-amber-300" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-indigo-950">
                  Kết quả phân tích ngữ nghĩa AI cho: &quot;{nlpQuery}&quot;
                </h3>
                <p className="text-[11px] text-indigo-700">
                  Phát hiện nhu cầu: <strong>{products.length} sản phẩm phù hợp</strong> 
                  {nlpIntent?.maxPriceMinor && ` • Ngân sách < ${new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(nlpIntent.maxPriceMinor)}`}
                </p>
              </div>
            </div>

            <button
              onClick={resetCatalog}
              className="px-3 py-1.5 rounded-xl bg-white hover:bg-slate-100 text-indigo-700 text-xs font-bold border border-indigo-200 flex items-center gap-1.5 shadow-2xs transition-colors shrink-0 cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Xóa bộ lọc AI</span>
            </button>
          </div>
        )}

        {/* Category Filter Pills & Section Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-2 border-b border-slate-200/80">
          <div>
            <h2 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight flex items-center gap-2">
              <span>Danh mục sản phẩm</span>
              <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-200 text-slate-700">
                {products.length}
              </span>
            </h2>
            <p className="text-xs text-slate-500">
              Dữ liệu được chuẩn hóa 3NF, gắn nhãn AI Tags và đồng bộ Vector Embeddings
            </p>
          </div>

          {/* Category Tabs */}
          <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto scrollbar-none pb-1">
            <button
              onClick={() => fetchProducts(undefined)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer shrink-0 ${
                selectedCategoryId === null
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200/80'
              }`}
            >
              Tất cả
            </button>

            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => fetchProducts(cat.id)}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer shrink-0 ${
                  selectedCategoryId === cat.id
                    ? 'bg-indigo-600 text-white shadow-xs shadow-indigo-600/20'
                    : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200/80'
                }`}
              >
                {cat.name}
              </button>
            ))}
          </div>
        </div>

        {/* Product Cards Grid */}
        {isLoadingProducts ? (
          <div className="py-20 text-center space-y-3">
            <Sparkles className="w-8 h-8 text-indigo-600 mx-auto animate-spin" />
            <p className="text-xs font-bold text-slate-500">Đang truy vấn cơ sở dữ liệu và xếp hạng AI...</p>
          </div>
        ) : products.length === 0 ? (
          <div className="py-20 text-center space-y-3 bg-white rounded-3xl border border-slate-200 p-8">
            <div className="w-16 h-16 rounded-full bg-slate-100 text-slate-400 mx-auto flex items-center justify-center">
              <SlidersHorizontal className="w-8 h-8" />
            </div>
            <h3 className="font-bold text-slate-800 text-base">Không tìm thấy sản phẩm phù hợp</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Không có sản phẩm nào khớp với tiêu chí tìm kiếm. Hãy thử với các từ khóa khác hoặc bấm Xóa bộ lọc.
            </p>
            <button
              onClick={resetCatalog}
              className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-colors cursor-pointer"
            >
              Xem tất cả sản phẩm
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}

      </main>

      {/* 4. Footer & Architectural Credits */}
      <footer className="mt-auto bg-slate-950 text-slate-400 text-xs border-t border-slate-800 py-10 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">
          <div className="space-y-1.5">
            <div className="flex items-center justify-center md:justify-start gap-2 text-white font-extrabold text-sm">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span>AI-Native Commerce Platform</span>
            </div>
            <p className="text-[11px] text-slate-500">
              Đề tài Dự Án Cuối Khóa môn NET108 — Trường Cao đẳng FPT Polytechnic
            </p>
            <p className="text-[10px] text-slate-600">
              Sinh viên thực hiện: Nguyễn Văn Khải • Giảng viên hướng dẫn môn NET108
            </p>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-4 text-[11px]">
            <span className="flex items-center gap-1 text-slate-300">
              <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" /> Waterfall SDLC (5 Giai đoạn)
            </span>
            <span>•</span>
            <span className="flex items-center gap-1 text-slate-300">
              <PackageCheck className="w-3.5 h-3.5 text-emerald-400" /> 15-Min Quote Lock
            </span>
            <span>•</span>
            <span className="flex items-center gap-1 text-slate-300">
              <CheckCircle2 className="w-3.5 h-3.5 text-purple-400" /> Idempotency Saga
            </span>
          </div>
        </div>
      </footer>

      {/* 5. Modals & Widgets */}
      <ProductModal />
      <CartDrawer />
      <CheckoutModal />
      <OrderSuccessModal />
      <AiAssistantWidget />
      <AdminDashboard />

    </div>
  );
};

export default App;
