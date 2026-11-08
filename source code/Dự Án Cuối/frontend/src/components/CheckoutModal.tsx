import React, { useState } from 'react';
import { 
  X, 
  ShieldCheck, 
  Lock, 
  QrCode, 
  Truck, 
  CreditCard, 
  Sparkles,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';
import { useCommerceStore } from '../store/useCommerceStore';

export const CheckoutModal: React.FC = () => {
  const {
    isCheckoutOpen,
    setCheckoutOpen,
    activeQuote,
    checkoutOrder,
    currentUser
  } = useCommerceStore();

  const [recipientName, setRecipientName] = useState(currentUser?.fullName || 'Nguyễn Văn Khải');
  const [shippingPhone, setShippingPhone] = useState(currentUser?.phone || '0987654321');
  const [shippingAddress, setShippingAddress] = useState('Toà nhà FPT Polytechnic, Phố Trịnh Văn Bô, Nam Từ Liêm, Hà Nội');
  const [paymentMethod, setPaymentMethod] = useState<'VIETQR' | 'COD'>('VIETQR');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  if (!isCheckoutOpen || !activeQuote) return null;

  const formatVND = (minor: number) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(minor);
  };

  const handleCheckout = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!shippingAddress.trim() || !shippingPhone.trim() || !recipientName.trim()) {
      setErrorMsg('Vui lòng điền đầy đủ thông tin giao hàng');
      return;
    }

    setIsSubmitting(true);
    setErrorMsg('');

    const res = await checkoutOrder({
      recipientName,
      shippingPhone,
      shippingAddress,
      paymentMethod
    });

    setIsSubmitting(false);

    if (!res.success) {
      setErrorMsg(res.error || 'Giao dịch thất bại. Vui lòng thử lại.');
    }
  };

  // Dynamic VietQR payment URL simulation
  const vietQrUrl = `https://img.vietqr.io/image/970422-0987654321-compact2.png?amount=${activeQuote.totalMinor}&addInfo=AINATIVE_${activeQuote.id.slice(0, 8)}&accountName=AI%20NATIVE%20COMMERCE`;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div 
        className="relative w-full max-w-2xl bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden animate-in fade-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 bg-slate-900 text-white flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
              <ShieldCheck className="w-5 h-5 text-indigo-400" />
            </div>
            <div>
              <h3 className="font-extrabold text-base">Thanh Toán An Toàn (Idempotency Saga)</h3>
              <p className="text-[11px] text-slate-400 font-mono">
                Quote ID: {activeQuote.id}
              </p>
            </div>
          </div>

          <button
            onClick={() => setCheckoutOpen(false)}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Form */}
        <form onSubmit={handleCheckout} className="p-6 space-y-6">
          
          {errorMsg && (
            <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Shipping Information */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Truck className="w-4 h-4 text-indigo-600" />
              Thông tin nhận hàng
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Họ và tên người nhận</label>
                <input
                  type="text"
                  required
                  value={recipientName}
                  onChange={(e) => setRecipientName(e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Số điện thoại liên hệ</label>
                <input
                  type="text"
                  required
                  value={shippingPhone}
                  onChange={(e) => setShippingPhone(e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-hidden"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Địa chỉ giao hàng</label>
              <textarea
                rows={2}
                required
                value={shippingAddress}
                onChange={(e) => setShippingAddress(e.target.value)}
                className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-hidden"
              />
            </div>
          </div>

          {/* Payment Method Selector */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <CreditCard className="w-4 h-4 text-indigo-600" />
              Phương thức thanh toán
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              
              {/* VietQR Option */}
              <div
                onClick={() => setPaymentMethod('VIETQR')}
                className={`p-3.5 rounded-2xl border cursor-pointer transition-all ${
                  paymentMethod === 'VIETQR'
                    ? 'border-indigo-600 bg-indigo-50/50 ring-2 ring-indigo-500/20'
                    : 'border-slate-200 hover:border-slate-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <QrCode className="w-5 h-5 text-indigo-600" />
                    <div>
                      <h5 className="text-xs font-bold text-slate-900">Quét mã VietQR</h5>
                      <p className="text-[10px] text-slate-500">Chuyển khoản 24/7 mọi ngân hàng</p>
                    </div>
                  </div>
                  {paymentMethod === 'VIETQR' && <CheckCircle2 className="w-4 h-4 text-indigo-600" />}
                </div>
              </div>

              {/* COD Option */}
              <div
                onClick={() => setPaymentMethod('COD')}
                className={`p-3.5 rounded-2xl border cursor-pointer transition-all ${
                  paymentMethod === 'COD'
                    ? 'border-indigo-600 bg-indigo-50/50 ring-2 ring-indigo-500/20'
                    : 'border-slate-200 hover:border-slate-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Truck className="w-5 h-5 text-indigo-600" />
                    <div>
                      <h5 className="text-xs font-bold text-slate-900">COD (Tiền mặt)</h5>
                      <p className="text-[10px] text-slate-500">Thanh toán khi nhận kiện hàng</p>
                    </div>
                  </div>
                  {paymentMethod === 'COD' && <CheckCircle2 className="w-4 h-4 text-indigo-600" />}
                </div>
              </div>

            </div>

            {/* If VietQR selected, preview dynamic QR code */}
            {paymentMethod === 'VIETQR' && (
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
                <img
                  src={vietQrUrl}
                  alt="VietQR Code"
                  className="w-32 h-32 rounded-xl border border-slate-300 bg-white p-1 shadow-xs"
                />
                <div className="space-y-1 text-xs">
                  <span className="font-bold text-slate-800">Quét mã QR để hoàn tất thanh toán</span>
                  <p className="text-slate-500 text-[11px]">
                    Hệ thống sẽ tự động xác thực và cập nhật trạng thái đơn hàng sang <strong className="text-emerald-600">CONFIRMED</strong> ngay khi ngân hàng báo có.
                  </p>
                  <p className="font-mono text-indigo-600 font-bold text-[11px] pt-1">
                    Số tiền: {formatVND(activeQuote.totalMinor)}
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Total & Submit Button */}
          <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
            <div>
              <span className="text-[11px] text-slate-400 block font-medium">Tổng thanh toán đơn</span>
              <span className="text-xl font-extrabold text-slate-900">
                {formatVND(activeQuote.totalMinor)}
              </span>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="py-3 px-6 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm flex items-center gap-2 shadow-lg shadow-indigo-600/25 transition-all disabled:opacity-50 cursor-pointer"
            >
              <ShieldCheck className="w-4 h-4" />
              <span>{isSubmitting ? 'Đang xác thực Saga...' : 'Xác nhận Đặt Hàng'}</span>
            </button>
          </div>

        </form>
      </div>
    </div>
  );
};
