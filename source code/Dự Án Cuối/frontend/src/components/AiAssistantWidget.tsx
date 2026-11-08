import React, { useState, useRef, useEffect } from 'react';
import { 
  Bot, 
  X, 
  Send, 
  Sparkles, 
  ShieldCheck, 
  ThumbsUp, 
  ThumbsDown, 
  ArrowRight,
  ShoppingBag,
  CornerDownLeft,
  Minimize2,
  Check,
  AlertCircle
} from 'lucide-react';
import { useCommerceStore } from '../store/useCommerceStore';
import { ActionApproval, Product } from '../types';

export const AiAssistantWidget: React.FC = () => {
  const {
    isAssistantOpen,
    setAssistantOpen,
    chatMessages,
    isChatLoading,
    sendChatMessage,
    handleActionApproval,
    setSelectedProduct
  } = useCommerceStore();

  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isAssistantOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages, isAssistantOpen]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputMessage.trim() && !isChatLoading) {
      sendChatMessage(inputMessage.trim());
      setInputMessage('');
    }
  };

  const handlePromptClick = (prompt: string) => {
    sendChatMessage(prompt);
  };

  const formatVND = (minor: number) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(minor);
  };

  return (
    <>
      {/* Floating Launcher Button */}
      {!isAssistantOpen && (
        <button
          onClick={() => setAssistantOpen(true)}
          className="fixed bottom-6 right-6 z-40 p-4 rounded-full bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 text-white shadow-xl shadow-indigo-600/35 hover:scale-110 active:scale-95 transition-all duration-300 group cursor-pointer"
          aria-label="Mở Trợ lý AI"
        >
          <div className="relative">
            <Bot className="w-6 h-6 animate-pulse" />
            <span className="w-3 h-3 rounded-full bg-emerald-400 absolute -top-1 -right-1 ring-2 ring-white animate-ping" />
            <span className="w-3 h-3 rounded-full bg-emerald-400 absolute -top-1 -right-1 ring-2 ring-white" />
          </div>
          <span className="absolute right-full mr-3 top-1/2 -translate-y-1/2 px-3 py-1.5 rounded-xl bg-slate-900 text-white text-xs font-semibold whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none shadow-lg">
            Trò chuyện với AI Shopping Agent ✨
          </span>
        </button>
      )}

      {/* Chat Window */}
      {isAssistantOpen && (
        <div className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-50 w-[94vw] sm:w-[420px] h-[600px] max-h-[85vh] bg-white rounded-3xl shadow-2xl border border-slate-200/80 flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-5 duration-200">
          
          {/* Header */}
          <div className="p-4 bg-gradient-to-r from-slate-950 via-indigo-950 to-slate-900 text-white flex items-center justify-between border-b border-indigo-900/40">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-2xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center ring-1 ring-indigo-400/30">
                <Bot className="w-5 h-5 text-indigo-300" />
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <h3 className="font-bold text-sm text-white">AI Shopping Assistant</h3>
                  <span className="px-1.5 py-0.2 rounded text-[9px] font-bold bg-indigo-500/30 text-indigo-300 border border-indigo-400/30">
                    HITL L2
                  </span>
                </div>
                <div className="flex items-center gap-1.5 text-[10px] text-slate-400">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  <span>Trợ lý thông minh đang hoạt động</span>
                </div>
              </div>
            </div>

            <button
              onClick={() => setAssistantOpen(false)}
              className="p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
            >
              <Minimize2 className="w-4 h-4" />
            </button>
          </div>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50/50">
            {chatMessages.map((msg) => (
              <div
                key={msg.id}
                className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} space-y-1.5`}
              >
                {/* Bubble */}
                <div
                  className={`max-w-[85%] rounded-2xl px-4 py-3 text-xs leading-relaxed shadow-xs ${
                    msg.role === 'user'
                      ? 'bg-indigo-600 text-white rounded-br-xs'
                      : msg.role === 'system'
                      ? 'bg-amber-50 text-amber-900 border border-amber-200/80'
                      : 'bg-white text-slate-800 border border-slate-200/80 rounded-bl-xs'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                </div>

                {/* HITL Action Approval Card */}
                {msg.proposedAction && (
                  <div className="w-[90%] p-3.5 rounded-2xl bg-indigo-50/90 border border-indigo-200 text-slate-800 space-y-2.5 shadow-sm">
                    <div className="flex items-center gap-1.5 text-indigo-700 font-bold text-xs">
                      <ShieldCheck className="w-4 h-4 text-indigo-600" />
                      <span>Đề xuất phê duyệt hành động (HITL)</span>
                    </div>

                    <p className="text-xs text-slate-700 font-medium">
                      {msg.proposedAction.description}
                    </p>

                    <div className="flex items-center gap-2 pt-1">
                      <button
                        onClick={() => handleActionApproval(msg.proposedAction!, true)}
                        className="flex-1 py-1.5 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-xs transition-colors cursor-pointer"
                      >
                        <Check className="w-3.5 h-3.5" />
                        <span>Xác nhận duyệt</span>
                      </button>

                      <button
                        onClick={() => handleActionApproval(msg.proposedAction!, false)}
                        className="py-1.5 px-3 rounded-xl bg-white hover:bg-rose-50 text-rose-600 font-semibold text-xs border border-slate-200 transition-colors cursor-pointer"
                      >
                        Từ chối
                      </button>
                    </div>
                  </div>
                )}

                {/* Suggested Products Mini Cards */}
                {msg.suggestedProducts && msg.suggestedProducts.length > 0 && (
                  <div className="w-[90%] space-y-1.5 pt-1">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                      Sản phẩm được đề xuất:
                    </span>
                    {msg.suggestedProducts.slice(0, 2).map((prod) => (
                      <div
                        key={prod.id}
                        onClick={() => setSelectedProduct(prod)}
                        className="p-2.5 rounded-xl bg-white border border-slate-200/80 hover:border-indigo-400 flex items-center justify-between gap-2.5 shadow-xs transition-all cursor-pointer group"
                      >
                        <img
                          src={prod.imageUrl || 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop&q=80'}
                          alt={prod.name}
                          className="w-10 h-10 rounded-lg object-cover bg-slate-100 shrink-0"
                        />
                        <div className="flex-1 min-w-0">
                          <h5 className="text-[11px] font-bold text-slate-900 truncate group-hover:text-indigo-600">
                            {prod.name}
                          </h5>
                          <span className="text-[11px] font-extrabold text-indigo-600">
                            {formatVND(prod.priceMinor)}
                          </span>
                        </div>
                        <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-indigo-600 group-hover:translate-x-0.5 transition-all" />
                      </div>
                    ))}
                  </div>
                )}

                {/* Suggested Action Quick Chips */}
                {msg.suggestedActions && (
                  <div className="flex flex-wrap gap-1 pt-1 max-w-[90%]">
                    {msg.suggestedActions.map((action, i) => (
                      <button
                        key={i}
                        onClick={() => handlePromptClick(action)}
                        className="px-2.5 py-1 rounded-full text-[10px] font-medium bg-white hover:bg-indigo-50 text-indigo-600 border border-slate-200 shadow-2xs transition-colors"
                      >
                        {action}
                      </button>
                    ))}
                  </div>
                )}

                <span className="text-[9px] text-slate-400 px-1 font-mono">
                  {msg.timestamp}
                </span>
              </div>
            ))}

            {isChatLoading && (
              <div className="flex items-center gap-2 text-xs text-slate-400 p-2">
                <Sparkles className="w-4 h-4 text-indigo-500 animate-spin" />
                <span>Trợ lý AI đang suy luận và phân tích kho hàng...</span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Box */}
          <form onSubmit={handleSend} className="p-3 bg-white border-t border-slate-200/80">
            <div className="relative flex items-center">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Nhắn tin cho trợ lý AI (hỏi giá, tư vấn, thêm vào giỏ)..."
                className="w-full pl-3.5 pr-10 py-2.5 bg-slate-100 focus:bg-white text-xs rounded-xl border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 outline-hidden text-slate-900"
              />
              <button
                type="submit"
                disabled={!inputMessage.trim() || isChatLoading}
                className="absolute right-1.5 p-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-40 transition-colors cursor-pointer"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </div>
          </form>

        </div>
      )}
    </>
  );
};
