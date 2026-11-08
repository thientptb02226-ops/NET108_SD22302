import React from 'react';
import { CheckCircle, Package, ArrowRight, Truck, Clock, Sparkles } from 'lucide-react';
import { useCommerceStore } from '../store/useCommerceStore';

export const OrderSuccessModal: React.FC = () => {
  const { lastCreatedOrder, setLastCreatedOrder } = useCommerceStore();

  if (!lastCreatedOrder) return null;

  const formatVND = (minor: number) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(minor);
  };

  const steps = [
    { key: 'CONFIRMED', label: 'Đã xác nhận', done: true },
    { key: 'PROCESSING', label: 'Đang chuẩn bị', done: false },
    { key: 'SHIPPED', label: 'Đang giao hàng', done: false },
    { key: 'DELIVERED', label: 'Giao thành công', done: false },
  ];

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/70 backdrop-blur-xs flex items-center justify-center p-4">
      <div 
        className="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl border border-slate-100 p-6 sm:p-8 text-center space-y-6 animate-in fade-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Success Icon */}
        <div className="w-16 h-16 mx-auto rounded-3xl bg-emerald-100 text-emerald-600 flex items-center justify-center ring-8 ring-emerald-50">
          <CheckCircle className="w-9 h-9" />
        </div>

        <div className="space-y-1.5">
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700">
            <Sparkles className="w-3.5 h-3.5 text-emerald-500" />
            <span>Giao dịch hoàn tất thành công!</span>
          </span>
          <h2 className="text-2xl font-black text-slate-900">Cảm ơn bạn đã đặt hàng</h2>
          <p className="text-xs text-slate-500">
            Mã đơn hàng: <strong className="text-indigo-600 font-mono text-sm">{lastCreatedOrder.orderNumber}</strong>
          </p>
        </div>

        {/* State Machine Pipeline */}
        <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 text-left space-y-3">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
            Hành trình đơn hàng (State Machine)
          </span>

          <div className="grid grid-cols-4 gap-1 text-center">
            {steps.map((st, i) => (
              <div key={st.key} className="space-y-1">
                <div className={`h-1.5 rounded-full ${st.done ? 'bg-emerald-500' : 'bg-slate-200'}`} />
                <span className={`text-[10px] block font-semibold ${st.done ? 'text-emerald-700' : 'text-slate-400'}`}>
                  {st.label}
                </span>
              </div>
            ))}
          </div>

          <div className="pt-2 border-t border-slate-200/60 text-xs text-slate-600 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Truck className="w-4 h-4 text-indigo-600" />
              <span>Giao hàng tiêu chuẩn:</span>
            </span>
            <strong className="text-slate-900">Dự kiến trong 24 giờ tới</strong>
          </div>
        </div>

        {/* Total & Button */}
        <div className="flex items-center justify-between text-xs pt-2">
          <span className="text-slate-500">Tổng tiền đã khóa:</span>
          <span className="text-base font-extrabold text-slate-900">
            {formatVND(lastCreatedOrder.totalMinor)}
          </span>
        </div>

        <button
          onClick={() => setLastCreatedOrder(null)}
          className="w-full py-3.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm flex items-center justify-center gap-2 shadow-md shadow-indigo-600/25 transition-all cursor-pointer"
        >
          <span>Tiếp tục khám phá sản phẩm</span>
          <ArrowRight className="w-4 h-4" />
        </button>

      </div>
    </div>
  );
};
