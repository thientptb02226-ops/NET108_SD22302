import React from 'react';
import { ShoppingBag, Sparkles, Eye, Check } from 'lucide-react';
import { Product } from '../types';
import { useCommerceStore } from '../store/useCommerceStore';

interface ProductCardProps {
  product: Product;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const { addToCart, setSelectedProduct } = useCommerceStore();
  const [isAdded, setIsAdded] = React.useState(false);

  const handleAddToCart = async (e: React.MouseEvent) => {
    e.stopPropagation();
    await addToCart(product.id, 1);
    setIsAdded(true);
    setTimeout(() => setIsAdded(false), 1500);
  };

  const formatVND = (minor: number) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(minor);
  };

  return (
    <div
      onClick={() => setSelectedProduct(product)}
      className="group relative flex flex-col h-full bg-white rounded-2xl border border-slate-200/90 shadow-xs hover:shadow-xl hover:border-indigo-400 transition-all duration-300 overflow-hidden cursor-pointer"
    >
      {/* Top badges: AI match score or Stock */}
      <div className="absolute top-3 left-3 right-3 flex items-center justify-between z-10 pointer-events-none">
        {product.matchScore ? (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-bold bg-indigo-600/95 text-white backdrop-blur-md shadow-xs">
            <Sparkles className="w-3 h-3 text-amber-300" />
            <span>Phù hợp {product.matchScore * 10}%</span>
          </span>
        ) : (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-slate-900/80 text-white backdrop-blur-md">
            {product.category?.name || 'Sản phẩm'}
          </span>
        )}

        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold shadow-2xs ${
          product.stockQty > 5 
            ? 'bg-emerald-100 text-emerald-800' 
            : product.stockQty > 0 
            ? 'bg-amber-100 text-amber-800' 
            : 'bg-rose-100 text-rose-800'
        }`}>
          {product.stockQty > 0 ? `Còn ${product.stockQty}` : 'Hết hàng'}
        </span>
      </div>

      {/* Uniform Product Image (Fixed 220px Height with object-cover) */}
      <div className="relative h-56 w-full overflow-hidden bg-slate-100 shrink-0 border-b border-slate-100">
        <img
          src={product.imageUrl || 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop&q=80'}
          alt={product.name}
          className="h-full w-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950/30 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <span className="px-3.5 py-1.5 rounded-full bg-white/95 text-slate-900 font-bold text-xs shadow-md backdrop-blur-md flex items-center gap-1.5 transform translate-y-2 group-hover:translate-y-0 transition-all">
            <Eye className="w-3.5 h-3.5 text-indigo-600" /> Xem chi tiết
          </span>
        </div>
      </div>

      {/* Product Content - Uniform Grid Rows */}
      <div className="flex flex-col flex-1 p-5 justify-between">
        
        <div className="space-y-2.5">
          {/* AI Tags Row - Fixed Height */}
          <div className="flex items-center gap-1.5 h-6 overflow-hidden">
            {product.aiTags && product.aiTags.length > 0 ? (
              product.aiTags.slice(0, 3).map((tag, idx) => (
                <span
                  key={idx}
                  className="px-2 py-0.5 rounded-md text-[10px] font-medium bg-indigo-50 text-indigo-700 truncate"
                >
                  #{tag}
                </span>
              ))
            ) : (
              <span className="text-[10px] text-slate-400">#chinh-hang</span>
            )}
          </div>

          {/* Product Title - Exactly 2 lines height (h-12) */}
          <h3 className="font-bold text-sm sm:text-base text-slate-900 line-clamp-2 h-12 leading-snug group-hover:text-indigo-600 transition-colors">
            {product.name}
          </h3>

          {/* Product Description - Exactly 2 lines height (h-10) */}
          <p className="text-xs text-slate-500 line-clamp-2 h-10 leading-relaxed">
            {product.description}
          </p>
        </div>

        {/* Footer: Price & Add To Cart Button - Strictly Aligned at Bottom */}
        <div className="mt-5 pt-3.5 border-t border-slate-100 flex items-center justify-between">
          <div className="min-w-0">
            <span className="text-[10px] text-slate-400 block font-medium uppercase tracking-wider">Giá niêm yết</span>
            <span className="text-base sm:text-lg font-black text-slate-900 truncate block">
              {formatVND(product.priceMinor)}
            </span>
          </div>

          <button
            onClick={handleAddToCart}
            disabled={product.stockQty <= 0}
            className={`px-3.5 py-2.5 rounded-xl font-bold text-xs flex items-center gap-1.5 transition-all shadow-xs shrink-0 ${
              isAdded
                ? 'bg-emerald-600 text-white'
                : 'bg-indigo-600 hover:bg-indigo-700 text-white disabled:bg-slate-200 disabled:text-slate-400'
            }`}
            title="Thêm vào giỏ hàng"
          >
            {isAdded ? (
              <>
                <Check className="w-4 h-4" />
                <span>Đã thêm</span>
              </>
            ) : (
              <>
                <ShoppingBag className="w-4 h-4" />
                <span>Chọn mua</span>
              </>
            )}
          </button>
        </div>

      </div>
    </div>
  );
};
