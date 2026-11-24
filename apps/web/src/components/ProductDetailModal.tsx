'use client';

import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { Product } from '../types';
import { formatCurrency } from './ProductCard';
import { fetchProductBySlug } from '../services/api';

interface ProductDetailModalProps {
  product: Product | null;
  onClose: () => void;
  onAddToCart: (product: Product, quantity: number) => void;
}

export const ProductDetailModal: React.FC<ProductDetailModalProps> = ({
  product: initialProduct,
  onClose,
  onAddToCart,
}) => {
  const [product, setProduct] = useState<Product | null>(initialProduct);
  const [activeImage, setActiveImage] = useState<string>('');
  const [quantity, setQuantity] = useState<number>(1);
  const [activeTab, setActiveTab] = useState<'specs' | 'desc' | 'reviews'>('specs');
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (initialProduct) {
      setProduct(initialProduct);
      setActiveImage(initialProduct.thumbnail);
      setQuantity(1);

      if (!initialProduct.specifications || initialProduct.specifications.length === 0) {
        setLoading(true);
        fetchProductBySlug(initialProduct.slug).then((fullData) => {
          if (fullData) {
            setProduct(fullData);
            if (fullData.thumbnail) setActiveImage(fullData.thumbnail);
          }
          setLoading(false);
        });
      }
    }
  }, [initialProduct]);

  if (!product) return null;

  // Group specifications by spec_group
  const groupedSpecs: Record<string, { key: string; value: string }[]> = {};
  if (product.specifications) {
    product.specifications.forEach((spec) => {
      if (!groupedSpecs[spec.spec_group]) {
        groupedSpecs[spec.spec_group] = [];
      }
      groupedSpecs[spec.spec_group].push({
        key: spec.spec_key,
        value: spec.spec_value,
      });
    });
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/40 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-4xl bg-white border border-gray-200 rounded-2xl shadow-xl overflow-hidden my-auto max-h-[92vh] flex flex-col">
        {/* Header Bar */}
        <div className="p-4 sm:p-5 border-b border-gray-200 flex items-center justify-between bg-gray-50">
          <div className="flex items-center gap-3">
            <span className="px-2.5 py-0.5 rounded bg-white border border-gray-300 text-gray-800 text-[10px] font-bold uppercase tracking-wider">
              {product.brand_name || 'CHÍNH HÃNG'}
            </span>
            <span className="text-xs text-gray-500 font-mono">Mã SKU: {product.sku}</span>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-gray-200 text-gray-500 hover:text-black transition"
            aria-label="Đóng"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-5 sm:p-8 overflow-y-auto space-y-8 flex-1">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
            {/* Gallery Left Column */}
            <div className="md:col-span-5 space-y-3">
              <div className="aspect-square rounded-xl bg-[#FAFAFA] border border-gray-200 p-6 flex items-center justify-center overflow-hidden">
                <img
                  src={activeImage || product.thumbnail}
                  alt={product.title}
                  className="max-h-full max-w-full object-contain"
                />
              </div>

              {/* Thumbnails */}
              {product.gallery && product.gallery.length > 1 && (
                <div className="flex gap-2 overflow-x-auto pb-1">
                  {product.gallery.map((img, idx) => (
                    <button
                      key={idx}
                      onClick={() => setActiveImage(img)}
                      className={`w-16 h-16 rounded-lg bg-[#FAFAFA] border p-1 overflow-hidden transition ${
                        activeImage === img ? 'border-gray-950 ring-1 ring-gray-950' : 'border-gray-200 hover:border-gray-400'
                      }`}
                    >
                      <img src={img} alt={`Hình ${idx + 1}`} className="w-full h-full object-contain" />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Product Right Column Info */}
            <div className="md:col-span-7 space-y-5">
              <div>
                <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider block mb-1">
                  {product.category_name || 'Thiết bị điện tử'}
                </span>
                <h1 className="text-xl sm:text-2xl font-bold text-gray-950 leading-snug">
                  {product.title}
                </h1>
                <div className="flex items-center gap-3 mt-2 text-xs text-gray-600">
                  <span>Đánh giá: <strong className="text-gray-900">{product.rating.toFixed(1)}/5.0</strong></span>
                  <span className="text-gray-300">•</span>
                  <span>{product.review_count} lượt đánh giá thực tế</span>
                  <span className="text-gray-300">•</span>
                  <span className="text-emerald-700 font-semibold">Tình trạng: Còn hàng ({product.stock})</span>
                </div>
              </div>

              {/* Price Box */}
              <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                <div className="flex items-baseline gap-3">
                  <span className="text-2xl sm:text-3xl font-extrabold text-gray-950 tracking-tight">
                    {formatCurrency(product.price)}
                  </span>
                  {product.original_price > product.price && (
                    <span className="text-sm text-gray-400 line-through">
                      {formatCurrency(product.original_price)}
                    </span>
                  )}
                  {product.discount_percent > 0 && (
                    <span className="text-xs font-bold px-2 py-0.5 rounded bg-rose-50 border border-rose-200 text-rose-700">
                      Tiết kiệm {product.discount_percent}%
                    </span>
                  )}
                </div>
                <p className="text-[11px] text-gray-500">Giá đã bao gồm thuế VAT và bảo hiểm vận chuyển toàn quốc.</p>
              </div>

              {/* Brief Description */}
              {product.brief_desc && (
                <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                  {product.brief_desc}
                </p>
              )}

              {/* Trust Badges - Text Only */}
              <div className="grid grid-cols-2 gap-2 text-[11px] text-gray-700 pt-2 border-t border-gray-100">
                <div className="p-2.5 rounded-lg border border-gray-200 bg-white">
                  <strong>Cam kết chính hãng:</strong> Phân phối chính ngạch, mới 100% nguyên seal.
                </div>
                <div className="p-2.5 rounded-lg border border-gray-200 bg-white">
                  <strong>Chính sách đổi mới:</strong> 1 đổi 1 trong 30 ngày nếu phát sinh lỗi kỹ thuật.
                </div>
                <div className="p-2.5 rounded-lg border border-gray-200 bg-white">
                  <strong>Giao hàng bảo hiểm:</strong> Miễn phí vận chuyển hỏa tốc toàn quốc.
                </div>
                <div className="p-2.5 rounded-lg border border-gray-200 bg-white">
                  <strong>Hỗ trợ kỹ thuật:</strong> Cài đặt phần mềm và hỗ trợ kỹ thuật trọn đời.
                </div>
              </div>

              {/* Add to Cart Actions */}
              <div className="pt-2 flex items-center gap-3">
                <div className="flex items-center border border-gray-300 rounded-lg bg-white">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="px-3 py-2 text-sm text-gray-600 hover:text-black font-semibold"
                  >
                    -
                  </button>
                  <span className="px-3 py-2 text-xs font-bold text-gray-900 min-w-8 text-center">
                    {quantity}
                  </span>
                  <button
                    onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                    className="px-3 py-2 text-sm text-gray-600 hover:text-black font-semibold"
                  >
                    +
                  </button>
                </div>

                <button
                  onClick={() => {
                    onAddToCart(product, quantity);
                    onClose();
                  }}
                  disabled={product.stock <= 0}
                  className="flex-1 py-3 px-6 bg-gray-950 hover:bg-black text-white text-xs font-semibold rounded-lg transition"
                >
                  Thêm vào giỏ hàng • {formatCurrency(product.price * quantity)}
                </button>
              </div>
            </div>
          </div>

          {/* Detailed Tabs: Specs / Description / Reviews */}
          <div className="border-t border-gray-200 pt-6">
            <div className="flex gap-4 border-b border-gray-200 pb-2 text-xs font-semibold">
              <button
                onClick={() => setActiveTab('specs')}
                className={`pb-2 border-b-2 transition ${
                  activeTab === 'specs' ? 'border-gray-950 text-gray-950 font-bold' : 'border-transparent text-gray-500 hover:text-gray-900'
                }`}
              >
                Thông số kỹ thuật chi tiết
              </button>
              <button
                onClick={() => setActiveTab('desc')}
                className={`pb-2 border-b-2 transition ${
                  activeTab === 'desc' ? 'border-gray-950 text-gray-950 font-bold' : 'border-transparent text-gray-500 hover:text-gray-900'
                }`}
              >
                Mô tả sản phẩm
              </button>
              <button
                onClick={() => setActiveTab('reviews')}
                className={`pb-2 border-b-2 transition ${
                  activeTab === 'reviews' ? 'border-gray-950 text-gray-950 font-bold' : 'border-transparent text-gray-500 hover:text-gray-900'
                }`}
              >
                Đánh giá từ khách hàng ({product.reviews?.length || product.review_count || 0})
              </button>
            </div>

            <div className="pt-4">
              {activeTab === 'specs' && (
                <div className="space-y-6">
                  {Object.keys(groupedSpecs).length > 0 ? (
                    Object.entries(groupedSpecs).map(([groupName, specs]) => (
                      <div key={groupName} className="space-y-2">
                        <h4 className="text-xs font-bold text-gray-900 uppercase tracking-wider">
                          {groupName}
                        </h4>
                        <div className="rounded-lg border border-gray-200 overflow-hidden text-xs">
                          {specs.map((s, idx) => (
                            <div
                              key={idx}
                              className={`grid grid-cols-12 p-3 ${
                                idx % 2 === 0 ? 'bg-gray-50/70' : 'bg-white'
                              } border-b border-gray-100 last:border-0`}
                            >
                              <div className="col-span-4 font-medium text-gray-600">{s.key}</div>
                              <div className="col-span-8 font-semibold text-gray-900">{s.value}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-xs text-gray-500">Thông số kỹ thuật đang được cập nhật từ nhà sản xuất.</p>
                  )}
                </div>
              )}

              {activeTab === 'desc' && (
                <div className="text-xs sm:text-sm text-gray-700 leading-relaxed space-y-4 max-w-3xl">
                  <p>{product.full_desc || product.brief_desc}</p>
                </div>
              )}

              {activeTab === 'reviews' && (
                <div className="space-y-4">
                  {product.reviews && product.reviews.length > 0 ? (
                    product.reviews.map((rev) => (
                      <div key={rev.id} className="p-4 rounded-xl border border-gray-200 bg-gray-50/50 space-y-2 text-xs">
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-gray-900">{rev.author_name}</span>
                          <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">
                            Đã xác thực mua hàng chính hãng
                          </span>
                        </div>
                        <div className="text-gray-900 font-semibold">Đánh giá: {rev.rating}/5 sao</div>
                        <p className="text-gray-600 leading-relaxed">{rev.comment}</p>
                      </div>
                    ))
                  ) : (
                    <div className="p-4 rounded-xl border border-gray-200 text-xs text-gray-500 text-center">
                      Chưa có đánh giá nào. Hãy là người đầu tiên trải nghiệm và chia sẻ cảm nhận!
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
