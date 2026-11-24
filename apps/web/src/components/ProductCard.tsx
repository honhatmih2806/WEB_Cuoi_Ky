'use client';

import React from 'react';
import { Product } from '../types';

interface ProductCardProps {
  product: Product;
  onSelectProduct: (product: Product) => void;
  onAddToCart: (product: Product) => void;
}

export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    maximumFractionDigits: 0,
  }).format(amount);
};

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onSelectProduct,
  onAddToCart,
}) => {
  return (
    <div className="group relative flex flex-col justify-between rounded-xl bg-white border border-gray-200 hover:border-gray-900 transition-all duration-200 hover:shadow-sm overflow-hidden">
      {/* Top Image Container */}
      <div className="relative aspect-square w-full bg-[#FAFAFA] p-6 flex items-center justify-center overflow-hidden border-b border-gray-100">
        {/* Badges (Text Only - No decorative icons) */}
        <div className="absolute top-3 left-3 z-10 flex flex-col gap-1 items-start">
          {product.badge && (
            <span className="px-2 py-0.5 bg-white border border-gray-300 text-gray-800 text-[9px] font-bold uppercase tracking-wider rounded">
              {product.badge}
            </span>
          )}
          {product.discount_percent > 0 && (
            <span className="px-2 py-0.5 bg-rose-50 border border-rose-200 text-rose-700 text-[9px] font-bold rounded">
              -{product.discount_percent}%
            </span>
          )}
        </div>

        {/* Quick View Overlay on Hover */}
        <button
          onClick={() => onSelectProduct(product)}
          className="absolute inset-0 bg-black/5 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center z-10"
        >
          <span className="px-3.5 py-1.5 rounded-md bg-white border border-gray-300 text-xs font-semibold text-gray-900 shadow-sm transform translate-y-1 group-hover:translate-y-0 transition">
            Xem chi tiết
          </span>
        </button>

        <img
          src={product.thumbnail}
          alt={product.title}
          className="h-full w-full object-contain group-hover:scale-105 transition-transform duration-300"
          loading="lazy"
        />
      </div>

      {/* Product Content Details */}
      <div className="p-4 sm:p-5 flex-1 flex flex-col justify-between space-y-3 bg-white">
        <div>
          {/* Brand & Stock Status */}
          <div className="flex items-center justify-between text-[11px] mb-1">
            <span className="font-semibold uppercase tracking-wider text-gray-500">
              {product.brand_name || 'CHÍNH HÃNG'}
            </span>
            <span className="text-gray-500 font-medium">
              Đánh giá: <strong className="text-gray-900">{product.rating.toFixed(1)}</strong> ({product.review_count})
            </span>
          </div>

          {/* Title */}
          <h3
            onClick={() => onSelectProduct(product)}
            className="text-sm font-semibold text-gray-950 group-hover:text-black transition-colors cursor-pointer line-clamp-2 leading-snug"
          >
            {product.title}
          </h3>

          {/* Key Specs Highlights (Text Only - No decorative icons) */}
          {product.key_specs && Object.keys(product.key_specs).length > 0 && (
            <div className="mt-2.5 flex flex-wrap gap-1">
              {Object.entries(product.key_specs).slice(0, 3).map(([key, val]) => (
                <span
                  key={key}
                  className="px-2 py-0.5 rounded bg-gray-100 text-gray-700 text-[10px] font-medium"
                >
                  {val}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Pricing & Cart Action */}
        <div className="pt-3 border-t border-gray-100 space-y-2.5">
          <div className="flex items-baseline justify-between">
            <div>
              <div className="text-base sm:text-lg font-bold text-gray-950 tracking-tight">
                {formatCurrency(product.price)}
              </div>
              {product.original_price > product.price && (
                <div className="text-xs text-gray-400 line-through">
                  {formatCurrency(product.original_price)}
                </div>
              )}
            </div>

            <div className="text-right">
              {product.stock > 0 ? (
                <span className="text-[11px] font-medium text-emerald-700">
                  Còn hàng ({product.stock})
                </span>
              ) : (
                <span className="text-[11px] font-medium text-rose-600">Tạm hết hàng</span>
              )}
            </div>
          </div>

          {/* Action Button */}
          <button
            onClick={() => onAddToCart(product)}
            disabled={product.stock <= 0}
            className={`w-full py-2.5 px-3 rounded-lg text-xs font-semibold transition-colors ${
              product.stock > 0
                ? 'bg-gray-950 hover:bg-black text-white'
                : 'bg-gray-100 text-gray-400 cursor-not-allowed'
            }`}
          >
            {product.stock > 0 ? 'Thêm vào giỏ hàng' : 'Hết hàng'}
          </button>
        </div>
      </div>
    </div>
  );
};
