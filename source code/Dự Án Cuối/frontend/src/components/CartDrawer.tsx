import React, { useState } from 'react';
import { 
  X, 
  Trash2, 
  ArrowRight, 
  Lock, 
  Clock, 
  ShieldCheck, 
  ShoppingBag, 
  Sparkles,
  AlertCircle
} from 'lucide-react';
import { useCommerceStore } from '../store/useCommerceStore';

export const CartDrawer: React.FC = () => {
  const {
    isCartOpen,
    setCartOpen,
    cart,
    updateCartItem,
    removeCartItem,
    createQuote,
    activeQuote,
    quoteTimeRemaining,
    setCheckoutOpen
  } = useCommerceStore();

  const [isGeneratingQuote, setIsGeneratingQuote] = useState(false);

  if (!isCartOpen) return null;

  const formatVND = (minor: number) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(minor);
  };

  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleGenerateQuote = async () => {
    setIsGeneratingQuote(true);
    await createQuote();
    setIsGeneratingQuote(false);
  };

  const handleProceedToCheckout = () => {
    setCartOpen(false);
    setCheckoutOpen(true);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-slate-900/50 backdrop-blur-xs transition-opacity"
        onClick={() => setCartOpen(false)}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white shadow-2xl flex flex-col justify-between border-l border-slate-200 animate-in slide-in-from-right duration-300">
          
          {/* Header */}
          <div className="p-6 border-b border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ShoppingBag className="w-5 h-5 text-indigo-600" />
              <h2 className="text-lg font-bold text-slate-900">Giỏ hàng của bạn</h2>
              {cart && (
                <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700">
                  {cart.items.reduce((s, i) => s + i.quantity, 0)} món
                </span>
              )}
            </div>

            <button
              onClick={() => setCartOpen(false)}
              className="p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Cart Items List */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {!cart || cart.items.length === 0 ? (
              <div className="py-16 text-center space-y-3">
                <div className="w-16 h-16 mx-auto rounded-full bg-slate-100 flex items-center justify-center text-slate-400">
                  <ShoppingBag className="w-8 h-8" />
                </div>
                <h3 className="font-bold text-slate-700">Giỏ hàng trống</h3>
                <p className="text-xs text-slate-400 max-w-xs mx-auto">
                  Hãy khám phá danh mục sản phẩm hoặc sử dụng Trợ lý AI để thêm sản phẩm phù hợp.
                </p>
              </div>
            ) : (
              cart.items.map((item) => (
                <div 
                  key={item.id}
                  className="flex gap-3.5 p-3 rounded-2xl bg-slate-50 border border-slate-100 items-center justify-between"
                >
                  <img
                    src={item.product.imageUrl || 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop&q=80'}
                    alt={item.product.name}
                    className="w-16 h-16 rounded-xl object-cover bg-white shrink-0 border border-slate-200/60"
                  />

                  <div className="flex-1 min-w-0">
                    <h4 className="text-xs font-bold text-slate-900 truncate">
                      {item.product.name}
                    </h4>
                    <span className="text-xs font-bold text-indigo-600 block mt-0.5">
                      {formatVND(item.unitPriceMinor)}
                    </span>

                    {/* Quantity Controls */}
                    <div className="flex items-center gap-2 mt-2">
                      <div className="flex items-center border border-slate-200 rounded-lg bg-white overflow-hidden">
                        <button
                          onClick={() => updateCartItem(item.id, Math.max(1, item.quantity - 1))}
                          className="px-2 py-0.5 text-xs text-slate-600 hover:bg-slate-100"
                        >
                          -
                        </button>
                        <span className="px-2 py-0.5 text-xs font-semibold text-slate-800">
                          {item.quantity}
                        </span>
                        <button
                          onClick={() => updateCartItem(item.id, item.quantity + 1)}
                          className="px-2 py-0.5 text-xs text-slate-600 hover:bg-slate-100"
                        >
                          +
                        </button>
                      </div>

                      <button
                        onClick={() => removeCartItem(item.id)}
                        className="p-1 text-slate-400 hover:text-rose-500 transition-colors"
                        title="Xóa món này"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                  <div className="text-right">
                    <span className="text-xs font-extrabold text-slate-900 block">
                      {formatVND(item.unitPriceMinor * item.quantity)}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer: Quote Lock & Checkout */}
          {cart && cart.items.length > 0 && (
            <div className="p-6 bg-slate-50 border-t border-slate-200 space-y-4">
              
              {/* Active Frozen Quote Card */}
              {activeQuote ? (
                <div className="p-3.5 rounded-2xl bg-indigo-900 text-white space-y-2 shadow-lg">
                  <div className="flex items-center justify-between text-xs font-bold">
                    <div className="flex items-center gap-1.5 text-amber-300">
                      <Lock className="w-3.5 h-3.5" />
                      <span>BÁO GIÁ ĐÃ ĐƯỢC ĐÓNG BĂNG</span>
                    </div>
                    <div className="flex items-center gap-1 text-emerald-300 font-mono">
                      <Clock className="w-3.5 h-3.5" />
                      <span>{formatTimer(quoteTimeRemaining)}</span>
                    </div>
                  </div>

                  <p className="text-[11px] text-slate-300 font-mono truncate">
                    Hash: {activeQuote.fingerprint.slice(0, 24)}...
                  </p>

                  <div className="space-y-1 text-xs pt-1 border-t border-indigo-800/80">
                    <div className="flex justify-between text-slate-300">
                      <span>Tạm tính:</span>
                      <span>{formatVND(activeQuote.subtotalMinor)}</span>
                    </div>
                    {activeQuote.discountMinor > 0 && (
                      <div className="flex justify-between text-emerald-300">
                        <span>Giảm giá AI Voucher:</span>
                        <span>-{formatVND(activeQuote.discountMinor)}</span>
                      </div>
                    )}
                    <div className="flex justify-between text-slate-300">
                      <span>Phí giao hàng:</span>
                      <span>{activeQuote.shippingMinor === 0 ? 'Miễn phí' : formatVND(activeQuote.shippingMinor)}</span>
                    </div>
                    <div className="flex justify-between text-slate-300">
                      <span>Thuế VAT (10%):</span>
                      <span>{formatVND(activeQuote.taxMinor)}</span>
                    </div>
                    <div className="flex justify-between font-bold text-white text-sm pt-1 border-t border-indigo-800">
                      <span>Tổng thanh toán:</span>
                      <span className="text-amber-300">{formatVND(activeQuote.totalMinor)}</span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="p-3.5 rounded-2xl bg-amber-50 border border-amber-200/80 text-amber-900 space-y-2">
                  <div className="flex items-start gap-2">
                    <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                    <div className="text-xs">
                      <strong className="block font-bold">Cần đóng băng báo giá trước khi đặt hàng</strong>
                      Cơ chế Enterprise Quote Lock bảo vệ giỏ hàng của bạn khỏi biến động giá và đảm bảo giữ tồn kho trong 15 phút.
                    </div>
                  </div>

                  <button
                    onClick={handleGenerateQuote}
                    disabled={isGeneratingQuote}
                    className="w-full py-2.5 px-3 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-sm transition-colors"
                  >
                    <Lock className="w-3.5 h-3.5" />
                    <span>{isGeneratingQuote ? 'Đang mã hóa bảng giá...' : 'Tạo Báo Giá Đóng Băng (15 Phút)'}</span>
                  </button>
                </div>
              )}

              {/* Checkout Button */}
              {activeQuote && (
                <button
                  onClick={handleProceedToCheckout}
                  className="w-full py-3.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/30 transition-all cursor-pointer"
                >
                  <ShieldCheck className="w-4 h-4" />
                  <span>Tiến hành Đặt hàng An toàn</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              )}

            </div>
          )}

        </div>
      </div>
    </div>
  );
};
