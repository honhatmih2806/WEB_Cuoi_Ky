'use client';

import React from 'react';
import { ShoppingBag, Search } from 'lucide-react';

interface NavbarProps {
  cartCount: number;
  onOpenCart: () => void;
  onOpenAdvisor: () => void;
  onOpenTracking: () => void;
  searchQuery: string;
  onSearchChange: (q: string) => void;
  selectedCategory: string;
  onSelectCategory: (categorySlug: string) => void;
  selectedBrand: string;
  onSelectBrand: (brandSlug: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  cartCount,
  onOpenCart,
  onOpenAdvisor,
  onOpenTracking,
  searchQuery,
  onSearchChange,
  selectedCategory,
  onSelectCategory,
  selectedBrand,
  onSelectBrand,
}) => {
  const categoriesList = [
    { slug: 'all', name: 'Tất cả sản phẩm' },
    { slug: 'laptops', name: 'Máy tính xách tay' },
    { slug: 'smartphones', name: 'Điện thoại' },
    { slug: 'tablets', name: 'Máy tính bảng' },
    { slug: 'audio', name: 'Âm thanh Hi-Fi' },
    { slug: 'monitors', name: 'Màn hình' },
    { slug: 'pc-components', name: 'Linh kiện & AI' },
    { slug: 'consoles', name: 'Máy chơi game' },
    { slug: 'smartwatches', name: 'Đồng hồ thông minh' },
    { slug: 'accessories', name: 'Phụ kiện cao cấp' },
    { slug: 'bundles', name: 'Combo ưu đãi' },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-gray-200 transition-all">
      {/* Top Announcement Bar: Clean Japanese Boutique Notification */}
      <div className="bg-gray-50 border-b border-gray-200/80 py-2 px-4 text-xs text-gray-600">
        <div className="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-2">
          <div className="flex items-center gap-4 text-[11px] font-medium tracking-wide text-gray-700">
            <span>Giao hàng bảo hiểm hỏa tốc toàn quốc</span>
            <span className="text-gray-300">•</span>
            <span>100% Sản phẩm chính hãng phân phối</span>
            <span className="hidden sm:inline text-gray-300">•</span>
            <span className="hidden sm:inline">Bảo hành 1 đổi 1 trong 30 ngày</span>
          </div>
          <div className="flex items-center gap-4 text-[11px]">
            <button
              onClick={onOpenTracking}
              className="text-gray-600 hover:text-black transition underline underline-offset-2 font-medium"
            >
              Tra cứu đơn hàng
            </button>
            <span className="text-gray-300">•</span>
            <span className="text-gray-500 font-medium">Hotline: 1800-8899 (Miễn phí 24/7)</span>
          </div>
        </div>
      </div>

      {/* Main Header */}
      <div className="max-w-7xl mx-auto px-4 py-3.5 flex items-center justify-between gap-4">
        {/* Brand Logo */}
        <div
          onClick={() => {
            onSelectCategory('all');
            onSelectBrand('all');
          }}
          className="cursor-pointer group flex items-center gap-3 select-none"
        >
          <div className="w-9 h-9 rounded-lg bg-gray-950 flex items-center justify-center text-white font-black text-sm tracking-tighter">
            TS
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold tracking-tight text-gray-950 group-hover:text-black">
                TECH STORE
              </span>
              <span className="text-[9px] font-bold tracking-widest px-1.5 py-0.5 border border-gray-300 text-gray-700 uppercase rounded">
                JAPAN
              </span>
            </div>
            <p className="text-[10px] text-gray-500 tracking-wider font-medium uppercase hidden sm:block">
              Premium Electronics & Computing
            </p>
          </div>
        </div>

        {/* Search Bar */}
        <div className="flex-1 max-w-md hidden md:block">
          <div className="relative">
            <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder="Tìm kiếm MacBook, iPhone 16, RTX 5090, Sony..."
              className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-xs text-gray-900 placeholder-gray-400 focus:outline-none focus:border-gray-900 focus:bg-white transition"
            />
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2.5 sm:gap-3">
          <button
            onClick={onOpenAdvisor}
            className="px-3.5 py-2 text-xs font-semibold text-gray-800 border border-gray-300 hover:border-gray-900 hover:bg-gray-50 rounded-lg transition"
          >
            Tư vấn cấu hình
          </button>

          <button
            onClick={onOpenCart}
            className="relative flex items-center gap-2 px-3.5 py-2 bg-gray-950 hover:bg-black text-white text-xs font-semibold rounded-lg transition"
          >
            <ShoppingBag className="w-4 h-4" />
            <span className="hidden sm:inline">Giỏ hàng</span>
            {cartCount > 0 && (
              <span className="w-5 h-5 rounded-full bg-white text-gray-950 text-[10px] font-black flex items-center justify-center">
                {cartCount}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Mobile Search Bar */}
      <div className="px-4 pb-3 md:hidden">
        <div className="relative">
          <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Tìm kiếm theo sản phẩm hoặc thương hiệu..."
            className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-xs text-gray-900 placeholder-gray-400 focus:outline-none focus:border-gray-900 focus:bg-white transition"
          />
        </div>
      </div>

      {/* Category Navigation Bar (Clean Typography - No Icons describing content) */}
      <nav className="border-t border-gray-100 bg-white">
        <div className="max-w-7xl mx-auto px-4 flex items-center gap-1 overflow-x-auto no-scrollbar py-1">
          {categoriesList.map((cat) => {
            const isActive = selectedCategory === cat.slug;
            return (
              <button
                key={cat.slug}
                onClick={() => {
                  onSelectCategory(cat.slug);
                  onSelectBrand('all');
                }}
                className={`whitespace-nowrap px-3.5 py-2 text-xs font-medium transition-colors border-b-2 ${
                  isActive
                    ? 'border-gray-950 text-gray-950 font-semibold'
                    : 'border-transparent text-gray-500 hover:text-gray-900 hover:border-gray-300'
                }`}
              >
                {cat.name}
              </button>
            );
          })}
        </div>
      </nav>
    </header>
  );
};
