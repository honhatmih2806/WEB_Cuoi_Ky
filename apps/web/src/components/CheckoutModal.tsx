'use client';

import React, { useState } from 'react';
import { X, Check } from 'lucide-react';
import { CartItem, Order } from '../types';
import { formatCurrency } from './ProductCard';
import { submitCheckout } from '../services/api';

interface CheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  items: CartItem[];
  voucherCode: string;
  onOrderSuccess: (order: Order) => void;
}

export const CheckoutModal: React.FC<CheckoutModalProps> = ({
  isOpen,
  onClose,
  items,
  voucherCode,
  onOrderSuccess,
}) => {
  const [formData, setFormData] = useState({
    name: 'Nguyễn Văn Hùng',
    email: 'hung.nguyen@techstore.vn',
    phone: '0988776655',
    address: 'Toà nhà Bitexco, 2 Hải Triều, P. Bến Nghé, Quận 1, TP. Hồ Chí Minh',
    paymentMethod: 'BANKING_QR', // COD, BANKING_QR
    notes: 'Giao trong giờ hành chính, gọi trước 15 phút.',
  });

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [confirmedOrder, setConfirmedOrder] = useState<Order | null>(null);
  const [copiedCode, setCopiedCode] = useState(false);

  if (!isOpen) return null;

  const subtotal = items.reduce((s, i) => s + i.product.price * i.quantity, 0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setLoading(true);

    const payload = {
      customer_name: formData.name,
      customer_email: formData.email,
      customer_phone: formData.phone,
      shipping_address: formData.address,
      payment_method: formData.paymentMethod,
      voucher_code: voucherCode || undefined,
      notes: formData.notes,
      items: items.map((i) => ({ product_id: i.product.id, quantity: i.quantity })),
    };

    const res = await submitCheckout(payload);
    setLoading(false);

    if (res.success && res.data) {
      setConfirmedOrder(res.data);
      onOrderSuccess(res.data);
    } else {
      setErrorMsg(res.error || 'Có lỗi xảy ra khi tạo đơn hàng.');
    }
  };

  const handleCopyOrderCode = () => {
    if (confirmedOrder) {
      navigator.clipboard.writeText(confirmedOrder.order_code);
      setCopiedCode(true);
      setTimeout(() => setCopiedCode(false), 2000);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/40 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-2xl bg-white border border-gray-200 rounded-2xl shadow-2xl overflow-hidden my-auto">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-gray-200 flex items-center justify-between bg-gray-50">
          <div>
            <h2 className="text-sm sm:text-base font-bold text-gray-950 uppercase tracking-wide">
              {confirmedOrder ? 'Đặt Hàng Thành Công' : 'Thanh Toán & Xác Nhận Đơn Hàng'}
            </h2>
            <p className="text-[11px] text-gray-500">
              {confirmedOrder ? 'Cảm ơn quý khách đã tin tưởng dịch vụ' : 'Hệ thống bảo mật giao dịch tiêu chuẩn PCI-DSS'}
            </p>
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
        <div className="p-5 sm:p-7">
          {confirmedOrder ? (
            /* Order Success Receipt View */
            <div className="space-y-6 text-center py-2">
              <div className="w-12 h-12 mx-auto rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700 font-bold text-lg">
                ✓
              </div>

              <div>
                <h3 className="text-lg font-bold text-gray-950">
                  Đơn Hàng Đã Được Tiếp Nhận!
                </h3>
                <p className="text-xs text-gray-600 mt-1 max-w-md mx-auto">
                  Mã vận đơn đã được gửi qua email <strong>{confirmedOrder.customer_email}</strong>. Chuyên viên sẽ gọi điện xác nhận trong 15 phút.
                </p>
              </div>

              {/* Order Code Box */}
              <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 max-w-md mx-auto space-y-2">
                <span className="text-[11px] text-gray-500 uppercase font-semibold">Mã Đơn Hàng Của Quý Khách</span>
                <div className="flex items-center justify-center gap-2">
                  <span className="text-base sm:text-lg font-mono font-bold text-gray-950">
                    {confirmedOrder.order_code}
                  </span>
                  <button
                    onClick={handleCopyOrderCode}
                    className="px-2 py-1 bg-white border border-gray-300 hover:border-gray-900 text-[10px] font-semibold text-gray-800 rounded transition"
                  >
                    {copiedCode ? 'Đã sao chép' : 'Sao chép'}
                  </button>
                </div>
              </div>

              {/* Banking QR payment section if chosen */}
              {confirmedOrder.payment_method === 'BANKING_QR' && (
                <div className="p-5 rounded-xl border border-gray-200 bg-white max-w-md mx-auto space-y-3 text-left">
                  <div className="text-xs font-bold text-gray-900 border-b border-gray-100 pb-2">
                    Thanh Toán Chuyển Khoản Nhanh VietQR 24/7
                  </div>

                  <div className="flex flex-col sm:flex-row items-center gap-4">
                    <img
                      src={`https://api.vietqr.io/image/970422-0988776655-compact2.jpg?amount=${confirmedOrder.final_amount}&addInfo=${confirmedOrder.order_code}&accountName=TECH%20STORE%20VIETNAM`}
                      alt="VietQR Chuyển Khoản"
                      className="w-36 h-36 border border-gray-200 rounded-lg p-1 bg-white object-contain"
                    />

                    <div className="text-xs space-y-1 text-gray-600 flex-1">
                      <div>Ngân hàng: <strong className="text-gray-900">MB Bank (Quân Đội)</strong></div>
                      <div>Số tài khoản: <strong className="text-gray-900 font-mono">0988776655</strong></div>
                      <div>Chủ tài khoản: <strong className="text-gray-900">TECH STORE VIETNAM LLC</strong></div>
                      <div>Số tiền: <strong className="text-gray-950 font-bold">{formatCurrency(confirmedOrder.final_amount)}</strong></div>
                      <div>Nội dung: <strong className="text-gray-950 font-mono">{confirmedOrder.order_code}</strong></div>
                    </div>
                  </div>
                  <p className="text-[10px] text-gray-500 italic text-center">
                    Hệ thống sẽ tự động xác nhận đơn hàng ngay khi nhận được biến động số dư.
                  </p>
                </div>
              )}

              <button
                onClick={onClose}
                className="px-6 py-2.5 bg-gray-950 hover:bg-black text-white text-xs font-semibold rounded-lg transition"
              >
                Hoàn Tất & Đóng
              </button>
            </div>
          ) : (
            /* Checkout Form */
            <form onSubmit={handleSubmit} className="space-y-5">
              {errorMsg && (
                <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs">
                  {errorMsg}
                </div>
              )}

              {/* Customer Info */}
              <div className="space-y-3">
                <h3 className="text-xs font-bold text-gray-900 uppercase tracking-wider">
                  Thông Tin Người Nhận Hàng
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="text-[11px] font-semibold text-gray-700 block mb-1">
                      Họ và Tên *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg text-xs text-gray-900 focus:bg-white focus:border-gray-900 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="text-[11px] font-semibold text-gray-700 block mb-1">
                      Số Điện Thoại Nhận Hàng *
                    </label>
                    <input
                      type="tel"
                      required
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                      className="w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg text-xs text-gray-900 focus:bg-white focus:border-gray-900 focus:outline-none"
                    />
                  </div>
                </div>

                <div>
                  <label className="text-[11px] font-semibold text-gray-700 block mb-1">
                    Email Nhận Hóa Đơn VAT & Mã Tra Cứu *
                  </label>
                  <input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg text-xs text-gray-900 focus:bg-white focus:border-gray-900 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="text-[11px] font-semibold text-gray-700 block mb-1">
                    Địa Chỉ Giao Hàng Chi Tiết *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.address}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                    className="w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg text-xs text-gray-900 focus:bg-white focus:border-gray-900 focus:outline-none"
                  />
                </div>
              </div>

              {/* Payment Methods */}
              <div className="space-y-3 pt-2 border-t border-gray-100">
                <h3 className="text-xs font-bold text-gray-900 uppercase tracking-wider">
                  Phương Thức Thanh Toán
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div
                    onClick={() => setFormData({ ...formData, paymentMethod: 'BANKING_QR' })}
                    className={`p-3.5 rounded-xl border cursor-pointer transition ${
                      formData.paymentMethod === 'BANKING_QR'
                        ? 'border-gray-950 bg-gray-50'
                        : 'border-gray-200 hover:border-gray-400 bg-white'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <strong className="text-xs font-bold text-gray-950">Chuyển Khoản VietQR</strong>
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">
                        Khuyên dùng
                      </span>
                    </div>
                    <p className="text-[11px] text-gray-500 mt-1">
                      Quét mã QR tự động qua ứng dụng mọi ngân hàng.
                    </p>
                  </div>

                  <div
                    onClick={() => setFormData({ ...formData, paymentMethod: 'COD' })}
                    className={`p-3.5 rounded-xl border cursor-pointer transition ${
                      formData.paymentMethod === 'COD'
                        ? 'border-gray-950 bg-gray-50'
                        : 'border-gray-200 hover:border-gray-400 bg-white'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <strong className="text-xs font-bold text-gray-950">Thanh Toán Khi Nhận (COD)</strong>
                      <span className="text-[10px] text-gray-500">Đồng kiểm</span>
                    </div>
                    <p className="text-[11px] text-gray-500 mt-1">
                      Kiểm tra nguyên seal trước khi thanh toán tiền mặt.
                    </p>
                  </div>
                </div>
              </div>

              {/* Submit Action */}
              <div className="pt-3 border-t border-gray-100 flex items-center justify-between">
                <div>
                  <span className="text-[11px] text-gray-500 block">Tổng thanh toán:</span>
                  <span className="text-base font-bold text-gray-950">{formatCurrency(subtotal)}</span>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="px-6 py-2.5 bg-gray-950 hover:bg-black text-white text-xs font-semibold rounded-lg shadow-sm transition disabled:opacity-50"
                >
                  {loading ? 'Đang tạo đơn hàng...' : 'Xác Nhận Đặt Hàng'}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
