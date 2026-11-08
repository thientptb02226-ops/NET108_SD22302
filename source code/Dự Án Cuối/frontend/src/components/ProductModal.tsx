import React, { useState } from 'react';
import { X, Sparkles, ShoppingBag, ShieldCheck, Truck, RotateCcw, Check, Cpu } from 'lucide-react';
import { useCommerceStore } from '../store/useCommerceStore';

export const ProductModal: React.FC = () => {
  const { selectedProduct, setSelectedProduct, addToCart, setAssistantOpen, sendChatMessage } = useCommerceStore();
  const [quantity, setQuantity] = useState(1);
  const [isAdded, setIsAdded] = useState(false);

  if (!selectedProduct) return null;

  const formatVND = (minor: number) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(minor);
  };

  const handleAddToCart = async () => {
    await addToCart(selectedProduct.id, quantity);
    setIsAdded(true);
    setTimeout(() => setIsAdded(false), 2000);
  };

  const handleAskAiAboutProduct = () => {
    setSelectedProduct(null);
    setAssistantOpen(true);
    sendChatMessage(`Tư vấn cho tôi chi tiết về sản phẩm ${selectedProduct.name}, có đáng mua không và ưu nhược điểm là gì?`);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div 
        className="relative w-full max-w-3xl bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden animate-in fade-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={() => setSelectedProduct(null)}
          className="absolute top-4 right-4 z-20 p-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 hover:text-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2">
          
          {/* Left: Product Image */}
          <div className="relative aspect-square md:aspect-auto bg-slate-100 flex items-center justify-center overflow-hidden">
            <img
              src={selectedProduct.imageUrl || 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop&q=80'}
              alt={selectedProduct.name}
              className="w-full h-full object-cover object-center"
            />
            {selectedProduct.matchScore && (
              <div className="absolute bottom-4 left-4 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold bg-indigo-600 text-white shadow-md">
                <Sparkles className="w-3.5 h-3.5 text-amber-300" />
                <span>AI Khuyên Dùng ({selectedProduct.matchScore * 10}% Match)</span>
              </div>
            )}
          </div>

          {/* Right: Product Details */}
          <div className="p-6 md:p-8 flex flex-col justify-between space-y-6 max-h-[85vh] overflow-y-auto">
            
            <div className="space-y-4">
              {/* Category & SKU */}
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span className="font-semibold text-indigo-600 uppercase tracking-wider">
                  {selectedProduct.category?.name}
                </span>
                <span>SKU: {selectedProduct.sku}</span>
              </div>

              {/* Title */}
              <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 leading-snug">
                {selectedProduct.name}
              </h2>

              {/* Price */}
              <div className="flex items-baseline gap-3">
                <span className="text-2xl sm:text-3xl font-black text-indigo-600">
                  {formatVND(selectedProduct.priceMinor)}
                </span>
                <span className="text-xs text-slate-400 font-medium">(Đã bao gồm VAT)</span>
              </div>

              {/* AI Tags */}
              {selectedProduct.aiTags && (
                <div className="flex flex-wrap gap-1.5">
                  {selectedProduct.aiTags.map((tag, i) => (
                    <span key={i} className="px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 text-slate-700">
                      #{tag}
                    </span>
                  ))}
                </div>
              )}

              {/* Specs Table */}
              {selectedProduct.specs && (
                <div className="space-y-2 pt-2 border-t border-slate-100">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                    <Cpu className="w-3.5 h-3.5 text-indigo-500" />
                    Thông số kỹ thuật cốt lõi
                  </h4>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {Object.entries(selectedProduct.specs).map(([k, v]) => (
                      <div key={k} className="p-2 rounded-lg bg-slate-50 border border-slate-100">
                        <span className="text-slate-400 block text-[10px] uppercase font-bold">{k}</span>
                        <span className="text-slate-800 font-semibold">{String(v)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Description */}
              <div className="space-y-1.5">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">Mô tả sản phẩm</h4>
                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                  {selectedProduct.description}
                </p>
              </div>

              {/* Guarantee badges */}
              <div className="grid grid-cols-3 gap-2 pt-2 text-[11px] text-slate-500">
                <div className="flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4 text-emerald-500 shrink-0" />
                  <span>Chính hãng 100%</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <RotateCcw className="w-4 h-4 text-indigo-500 shrink-0" />
                  <span>Đổi trả 7 ngày</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Truck className="w-4 h-4 text-blue-500 shrink-0" />
                  <span>Giao hỏa tốc 2h</span>
                </div>
              </div>
            </div>

            {/* Bottom Actions */}
            <div className="space-y-3 pt-4 border-t border-slate-100">
              
              {/* AI Advice Shortcut */}
              <button
                onClick={handleAskAiAboutProduct}
                className="w-full py-2 px-3 rounded-xl bg-purple-50 hover:bg-purple-100 text-purple-700 text-xs font-bold flex items-center justify-center gap-1.5 transition-colors"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Hỏi Trợ lý AI về sản phẩm này</span>
              </button>

              <div className="flex items-center gap-3">
                {/* Quantity */}
                <div className="flex items-center border border-slate-200 rounded-xl overflow-hidden bg-slate-50">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="px-3 py-2.5 text-slate-600 hover:bg-slate-200 font-bold transition-colors"
                  >
                    -
                  </button>
                  <span className="px-3 py-2.5 text-sm font-bold text-slate-800 min-w-[36px] text-center">
                    {quantity}
                  </span>
                  <button
                    onClick={() => setQuantity(quantity + 1)}
                    className="px-3 py-2.5 text-slate-600 hover:bg-slate-200 font-bold transition-colors"
                  >
                    +
                  </button>
                </div>

                {/* Add to Cart Button */}
                <button
                  onClick={handleAddToCart}
                  disabled={selectedProduct.stockQty <= 0}
                  className={`flex-1 py-3 px-5 rounded-xl font-bold text-sm flex items-center justify-center gap-2 shadow-md transition-all ${
                    isAdded
                      ? 'bg-emerald-600 text-white'
                      : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-indigo-500/20'
                  }`}
                >
                  {isAdded ? (
                    <>
                      <Check className="w-4 h-4" />
                      <span>Đã thêm vào giỏ!</span>
                    </>
                  ) : (
                    <>
                      <ShoppingBag className="w-4 h-4" />
                      <span>Thêm vào giỏ ({formatVND(selectedProduct.priceMinor * quantity)})</span>
                    </>
                  )}
                </button>
              </div>

            </div>

          </div>

        </div>

      </div>
    </div>
  );
};
