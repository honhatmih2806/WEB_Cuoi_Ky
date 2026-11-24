'use client';

import React, { useState } from 'react';
import { X, Trash2, ShoppingBag } from 'lucide-react';
import { CartItem } from '../types';
import { formatCurrency } from './ProductCard';

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  items: CartItem[];
  onUpdateQuantity: (productId: string, quantity: number) => void;
  onRemoveItem: (productId: string) => void;
  onOpenCheckout: (voucher: string) => void;
}

export const CartDrawer: React.FC<CartDrawerProps> = ({
  isOpen,
  onClose,
  items,
  onUpdateQuantity,
  onRemoveItem,
  onOpenCheckout,
}) => {
  const [voucherCode, setVoucherCode] = useState<string>('');
  const [appliedVoucher, setAppliedVoucher] = useState<string>('');
  const [voucherError, setVoucherError] = useState<string>('');

  if (!isOpen) return null;

  const subtotal = items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);

  // Voucher discount calculation
  let discount = 0;
  if (appliedVoucher === 'TITANVIP') {
    discount = Math.min(Math.round(subtotal * 0.05), 3000000);
  } else if (appliedVoucher === 'LUXURY' || appliedVoucher === 'SYNERGY') {
    discount = Math.min(Math.round(subtotal * 0.10), 6000000);
  } else if (appliedVoucher === 'TECHSTORE' && subtotal >= 20000000) {
    discount = 1000000;
  }

  const finalTotal = Math.max(0, subtotal - discount);

  const handleApplyVoucher = () => {
    setVoucherError('');
    const code = voucherCode.trim().toUpperCase();
    if (!code) {
      setAppliedVoucher('');
      return;
    }
    if (code === 'TITANVIP' || code === 'LUXURY' || code === 'SYNERGY' || code === 'TECHSTORE') {
      setAppliedVoucher(code);
    } else {
      setVoucherError('Mã không hợp lệ. Gợi ý: TITANVIP (giảm 5%), LUXURY (giảm 10%)');
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div
        onClick={onClose}
        className="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity"
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white border-l border-gray-200 shadow-2xl flex flex-col justify-between">
          {/* Header */}
          <div className="p-5 border-b border-gray-200 flex items-center justify-between bg-gray-50">
            <div className="flex items-center gap-2.5">
              <ShoppingBag className="w-4 h-4 text-gray-900" />
              <h2 className="text-sm font-bold text-gray-950 uppercase tracking-wide">
                Giỏ Hàng Mua Sắm
              </h2>
              <span className="text-[11px] bg-gray-200 text-gray-800 px-2 py-0.5 rounded-full font-bold">
                {items.length} món
              </span>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg hover:bg-gray-200 text-gray-500 hover:text-black transition"
              aria-label="Đóng"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Cart Item List */}
          <div className="p-5 flex-1 overflow-y-auto divide-y divide-gray-100 space-y-4">
            {items.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 space-y-3">
                <div className="w-14 h-14 rounded-2xl bg-gray-100 flex items-center justify-center text-gray-400">
                  <ShoppingBag className="w-6 h-6" />
                </div>
                <h3 className="text-sm font-bold text-gray-900">Giỏ hàng của bạn đang trống</h3>
                <p className="text-xs text-gray-500 max-w-xs">
                  Khám phá các thiết bị điện tử cao cấp MacBook, iPhone, RTX, Sony và tai nghe Hi-Fi để thêm vào giỏ.
                </p>
                <button
                  onClick={onClose}
                  className="mt-2 px-4 py-2 bg-gray-950 hover:bg-black text-xs font-semibold text-white rounded-lg transition"
                >
                  Tiếp tục xem sản phẩm
                </button>
              </div>
            ) : (
              items.map((item) => (
                <div key={item.product.id} className="pt-4 first:pt-0 flex gap-3.5 items-start">
                  {/* Thumbnail */}
                  <div className="w-20 h-20 rounded-lg bg-[#FAFAFA] border border-gray-200 p-2 flex-shrink-0 flex items-center justify-center">
                    <img
                      src={item.product.thumbnail}
                      alt={item.product.title}
                      className="max-h-full max-w-full object-contain"
                    />
                  </div>

                  {/* Info */}
                  <div className="flex-1 min-w-0 space-y-1.5">
                    <div className="text-[10px] text-gray-500 font-semibold uppercase tracking-wider">
                      {item.product.brand_name || 'CHÍNH HÃNG'}
                    </div>
                    <h4 className="text-xs font-semibold text-gray-900 line-clamp-2 leading-snug">
                      {item.product.title}
                    </h4>
                    <div className="text-xs font-bold text-gray-950">
                      {formatCurrency(item.product.price)}
                    </div>

                    {/* Stepper & Remove */}
                    <div className="flex items-center justify-between pt-1">
                      <div className="flex items-center border border-gray-300 rounded bg-white">
                        <button
                          onClick={() => onUpdateQuantity(item.product.id, item.quantity - 1)}
                          className="px-2.5 py-0.5 text-xs text-gray-600 hover:text-black font-semibold"
                        >
                          -
                        </button>
                        <span className="px-2 text-xs font-bold text-gray-900 min-w-6 text-center">
                          {item.quantity}
                        </span>
                        <button
                          onClick={() => onUpdateQuantity(item.product.id, item.quantity + 1)}
                          className="px-2.5 py-0.5 text-xs text-gray-600 hover:text-black font-semibold"
                        >
                          +
                        </button>
                      </div>

                      <button
                        onClick={() => onRemoveItem(item.product.id)}
                        className="text-gray-400 hover:text-rose-600 p-1 transition"
                        title="Xóa khỏi giỏ"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer & Checkout Action */}
          {items.length > 0 && (
            <div className="p-5 border-t border-gray-200 bg-gray-50 space-y-4">
              {/* Voucher Code Box */}
              <div className="space-y-1.5">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={voucherCode}
                    onChange={(e) => setVoucherCode(e.target.value)}
                    placeholder="Nhập mã ưu đãi (TITANVIP, LUXURY)"
                    className="flex-1 px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-xs uppercase placeholder-gray-400 focus:outline-none focus:border-gray-900"
                  />
                  <button
                    onClick={handleApplyVoucher}
                    className="px-3.5 py-1.5 bg-gray-900 hover:bg-black text-white text-xs font-semibold rounded-lg transition"
                  >
                    Áp dụng
                  </button>
                </div>
                {appliedVoucher && (
                  <p className="text-[11px] text-emerald-700 font-semibold">
                    Đã kích hoạt mã {appliedVoucher}
                  </p>
                )}
                {voucherError && (
                  <p className="text-[11px] text-rose-600 font-medium">{voucherError}</p>
                )}
              </div>

              {/* Price Breakdown */}
              <div className="space-y-1.5 text-xs border-t border-gray-200 pt-3">
                <div className="flex justify-between text-gray-600">
                  <span>Tạm tính ({items.length} món):</span>
                  <span className="font-semibold text-gray-900">{formatCurrency(subtotal)}</span>
                </div>
                {discount > 0 && (
                  <div className="flex justify-between text-emerald-700 font-medium">
                    <span>Ưu đãi voucher ({appliedVoucher}):</span>
                    <span>-{formatCurrency(discount)}</span>
                  </div>
                )}
                <div className="flex justify-between text-gray-600">
                  <span>Vận chuyển bảo hiểm hỏa tốc:</span>
                  <span className="font-semibold text-emerald-700">Miễn phí toàn quốc</span>
                </div>
                <div className="flex justify-between text-sm font-bold text-gray-950 pt-2 border-t border-gray-200">
                  <span>Tổng thanh toán:</span>
                  <span className="text-base text-gray-950">{formatCurrency(finalTotal)}</span>
                </div>
              </div>

              {/* Checkout Button */}
              <button
                onClick={() => onOpenCheckout(appliedVoucher)}
                className="w-full py-3 bg-gray-950 hover:bg-black text-white text-xs font-semibold rounded-lg shadow-sm transition"
              >
                Tiến hành đặt hàng • {formatCurrency(finalTotal)}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
