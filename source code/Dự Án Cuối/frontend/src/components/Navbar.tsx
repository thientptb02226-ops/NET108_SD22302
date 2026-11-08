import React, { useState } from 'react';
import { 
  Sparkles, 
  Search, 
  ShoppingCart, 
  Bot, 
  ShieldCheck, 
  User as UserIcon, 
  RotateCcw,
  SlidersHorizontal,
  ChevronDown
} from 'lucide-react';
import { useCommerceStore } from '../store/useCommerceStore';

export const Navbar: React.FC = () => {
  const {
    currentRole,
    switchRole,
    cartCount,
    setCartOpen,
    setAssistantOpen,
    setAdminOpen,
    executeNlpSearch,
    resetCatalog,
    nlpQuery,
    isNlpSearching
  } = useCommerceStore();

  const [searchInput, setSearchInput] = useState('');
  const [showRoleDropdown, setShowRoleDropdown] = useState(false);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim()) {
      executeNlpSearch(searchInput.trim());
    }
  };

  const handleQuickPrompt = (prompt: string) => {
    setSearchInput(prompt);
    executeNlpSearch(prompt);
  };

  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-slate-200/80 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20 gap-4">
          
          {/* Logo & Brand */}
          <div className="flex items-center gap-3 cursor-pointer shrink-0" onClick={resetCatalog}>
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/25 ring-2 ring-indigo-400/30">
              <Sparkles className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 bg-clip-text text-transparent">
                  AI-Native
                </span>
                <span className="px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wider bg-indigo-100 text-indigo-700 uppercase">
                  Commerce
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium">FPT Poly NET108 Final Project</p>
            </div>
          </div>

          {/* AI NLP Search Bar */}
          <div className="flex-1 max-w-2xl hidden md:block">
            <form onSubmit={handleSearchSubmit} className="relative">
              <div className="relative flex items-center">
                <input
                  type="text"
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  placeholder="Tìm kiếm bằng AI: 'laptop mỏng nhẹ dưới 35 triệu', 'tai nghe chống ồn'..."
                  className="w-full pl-11 pr-24 py-2.5 bg-slate-100/80 hover:bg-slate-100 focus:bg-white text-sm rounded-full border border-slate-300/80 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition-all outline-hidden text-slate-900 placeholder:text-slate-400"
                />
                <Search className="w-4 h-4 text-slate-400 absolute left-4 pointer-events-none" />
                
                <button
                  type="submit"
                  disabled={isNlpSearching}
                  className="absolute right-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-full flex items-center gap-1.5 shadow-xs transition-colors disabled:opacity-50"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>{isNlpSearching ? 'Đang phân tích...' : 'Tìm bằng AI'}</span>
                </button>
              </div>
            </form>

            {/* Quick Prompt Suggestions */}
            <div className="flex items-center gap-2 mt-1.5 overflow-x-auto text-[11px] text-slate-500 scrollbar-none">
              <span className="text-slate-400 flex items-center gap-1">
                <SlidersHorizontal className="w-3 h-3" /> Gợi ý:
              </span>
              <button 
                onClick={() => handleQuickPrompt('laptop mỏng nhẹ dưới 35 triệu')} 
                className="hover:text-indigo-600 hover:underline cursor-pointer transition-colors"
              >
                Laptop mỏng nhẹ &lt; 35tr
              </button>
              <span>•</span>
              <button 
                onClick={() => handleQuickPrompt('tai nghe chống ồn cao cấp')} 
                className="hover:text-indigo-600 hover:underline cursor-pointer transition-colors"
              >
                Tai nghe chống ồn
              </button>
              <span>•</span>
              <button 
                onClick={() => handleQuickPrompt('bàn phím cơ lập trình')} 
                className="hover:text-indigo-600 hover:underline cursor-pointer transition-colors"
              >
                Bàn phím cơ lập trình
              </button>
            </div>
          </div>

          {/* Right Action Controls */}
          <div className="flex items-center gap-3">
            
            {/* Role Switcher Demo */}
            <div className="relative">
              <button
                onClick={() => setShowRoleDropdown(!showRoleDropdown)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 shadow-2xs transition-colors"
              >
                <ShieldCheck className="w-3.5 h-3.5 text-indigo-600" />
                <span className="font-semibold">{currentRole}</span>
                <ChevronDown className="w-3 h-3 text-slate-400" />
              </button>

              {showRoleDropdown && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-xl border border-slate-100 py-1.5 z-50 animate-in fade-in slide-in-from-top-2">
                  <div className="px-3 py-1 border-b border-slate-100 text-[10px] font-bold text-slate-400 uppercase">
                    Chuyển đổi vai trò Demo
                  </div>
                  {(['CUSTOMER', 'MERCHANT', 'ADMIN'] as const).map((r) => (
                    <button
                      key={r}
                      onClick={() => {
                        switchRole(r);
                        setShowRoleDropdown(false);
                      }}
                      className={`w-full text-left px-3 py-2 text-xs font-medium flex items-center justify-between hover:bg-indigo-50 transition-colors ${
                        currentRole === r ? 'text-indigo-600 bg-indigo-50/50 font-bold' : 'text-slate-700'
                      }`}
                    >
                      <span>{r === 'CUSTOMER' ? 'Khách hàng (Customer)' : r === 'MERCHANT' ? 'Nhà bán lẻ (Merchant)' : 'Quản trị viên (Admin)'}</span>
                      {currentRole === r && <span className="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Admin Portal Toggle */}
            {currentRole === 'ADMIN' && (
              <button
                onClick={() => setAdminOpen(true)}
                className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-900 text-white hover:bg-slate-800 transition-colors shadow-xs"
              >
                Bảng điều khiển Admin
              </button>
            )}

            {/* Floating Assistant Launcher */}
            <button
              onClick={() => setAssistantOpen(true)}
              className="relative px-3.5 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-xs font-semibold flex items-center gap-1.5 shadow-md shadow-indigo-500/20 hover:brightness-110 transition-all cursor-pointer"
            >
              <Bot className="w-4 h-4 animate-bounce" />
              <span className="hidden sm:inline">Trợ lý AI</span>
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping absolute -top-0.5 -right-0.5" />
              <span className="w-2 h-2 rounded-full bg-emerald-400 absolute -top-0.5 -right-0.5" />
            </button>

            {/* Cart Trigger */}
            <button
              onClick={() => setCartOpen(true)}
              className="relative p-2.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 shadow-2xs transition-colors cursor-pointer"
              aria-label="Giỏ hàng"
            >
              <ShoppingCart className="w-5 h-5 text-slate-700" />
              {cartCount > 0 && (
                <span className="absolute -top-1.5 -right-1.5 w-5 h-5 bg-indigo-600 text-white text-[11px] font-bold rounded-full flex items-center justify-center shadow-xs ring-2 ring-white animate-scale-in">
                  {cartCount}
                </span>
              )}
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};
