import React from 'react';
import { 
  Sparkles, 
  ShieldCheck, 
  Clock, 
  Zap, 
  Bot, 
  ArrowRight,
  Cpu,
  Layers
} from 'lucide-react';
import { useCommerceStore } from '../store/useCommerceStore';

export const HeroBanner: React.FC = () => {
  const { setAssistantOpen, executeNlpSearch } = useCommerceStore();

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900 text-white py-14 px-4 sm:px-6 lg:px-8 border-b border-indigo-900/50">
      
      {/* Background Decorative Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e1b4b_1px,transparent_1px),linear-gradient(to_bottom,#1e1b4b_1px,transparent_1px)] bg-[size:3.5rem_3.5rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-40 pointer-events-none" />

      <div className="relative max-w-7xl mx-auto flex flex-col lg:flex-row items-center justify-between gap-10">
        
        {/* Left Column: Heading & Value Proposition */}
        <div className="max-w-2xl space-y-5 text-center lg:text-left">
          
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold backdrop-blur-md">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400 animate-spin" style={{ animationDuration: '6s' }} />
            <span>Kiến trúc Thương mại Điện tử AI-Native Chuẩn Enterprise</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
            Mua sắm Thông minh với <br />
            <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400 bg-clip-text text-transparent">
              Trợ lý AI Tự động hóa (HITL)
            </span>
          </h1>

          <p className="text-sm sm:text-base text-slate-300 leading-relaxed max-w-xl">
            Tích hợp mô hình ngôn ngữ lớn (LLM), khóa giá an toàn <strong className="text-white">15 phút</strong> (Quote Lock Fingerprint), và cơ chế chống trùng lặp giao dịch <strong className="text-white">Idempotency Saga</strong>.
          </p>

          {/* Call to Actions */}
          <div className="flex flex-wrap items-center justify-center lg:justify-start gap-3 pt-2">
            <button
              onClick={() => setAssistantOpen(true)}
              className="px-5 py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-bold text-sm flex items-center gap-2 shadow-lg shadow-indigo-500/25 transition-all transform hover:-translate-y-0.5 cursor-pointer"
            >
              <Bot className="w-4 h-4" />
              <span>Trò chuyện với Trợ lý AI</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => executeNlpSearch('laptop mỏng nhẹ pin trâu')}
              className="px-5 py-3 rounded-xl bg-white/10 hover:bg-white/15 text-white font-semibold text-sm border border-white/20 backdrop-blur-md transition-all cursor-pointer"
            >
              Xem Demo Tìm kiếm NLP
            </button>
          </div>

        </div>

        {/* Right Column: Architectural Highlights Cards */}
        <div className="grid grid-cols-2 gap-3.5 w-full lg:max-w-md">
          
          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md space-y-1.5 hover:border-indigo-500/50 transition-colors">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
              <Clock className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-white">Khóa Báo Giá 15 Phút</h4>
            <p className="text-xs text-slate-400 leading-snug">
              Bảo lưu giá và chiết khấu với chữ ký số SHA-256 fingerprint.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md space-y-1.5 hover:border-purple-500/50 transition-colors">
            <div className="w-8 h-8 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-white">Idempotency Saga</h4>
            <p className="text-xs text-slate-400 leading-snug">
              Ngăn chặn thanh toán lặp 100% nhờ Request Key header.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md space-y-1.5 hover:border-pink-500/50 transition-colors">
            <div className="w-8 h-8 rounded-lg bg-pink-500/20 text-pink-400 flex items-center justify-center">
              <Zap className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-white">NLP Vector Search</h4>
            <p className="text-xs text-slate-400 leading-snug">
              Tìm theo ngữ cảnh và thuộc tính AI (mỏng nhẹ, pin trâu).
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md space-y-1.5 hover:border-emerald-500/50 transition-colors">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
              <Layers className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-bold text-white">HITL Action Router</h4>
            <p className="text-xs text-slate-400 leading-snug">
              AI đề xuất hành động, người dùng bấm duyệt trước khi ghi.
            </p>
          </div>

        </div>

      </div>
    </div>
  );
};
