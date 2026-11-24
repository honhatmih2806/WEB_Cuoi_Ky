'use client';

import React, { useState } from 'react';
import { X, Search } from 'lucide-react';
import { Order } from '../types';
import { formatCurrency } from './ProductCard';
import { trackOrder } from '../services/api';

interface OrderTrackingModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const OrderTrackingModal: React.FC<OrderTrackingModalProps> = ({ isOpen, onClose }) => {
  const [orderCode, setOrderCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [order, setOrder] = useState<Order | null>(null);
  const [errorMsg, setErrorMsg] = useState('');

  if (!isOpen) return null;

  const handleTrack = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!orderCode.trim()) return;
    setLoading(true);
    setErrorMsg('');
    setOrder(null);

    const res = await trackOrder(orderCode.trim());
    setLoading(false);
    if (res.success && res.data) {
      setOrder(res.data);
    } else {
      setErrorMsg(res.error || 'Không tìm thấy đơn hàng với mã này trong hệ thống.');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/40 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-xl bg-white border border-gray-200 rounded-2xl shadow-xl overflow-hidden my-auto">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-gray-200 flex items-center justify-between bg-gray-50">
          <div>
            <h2 className="text-sm font-bold text-gray-950 uppercase tracking-wide">
              Tra Cứu Vận Đơn & Trạng Thái
            </h2>
            <p className="text-[11px] text-gray-500">Kiểm tra tiến độ giao hàng hỏa tốc toàn quốc</p>
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
        <div className="p-5 sm:p-7 space-y-6">
          <form onSubmit={handleTrack} className="flex gap-2">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={orderCode}
                onChange={(e) => setOrderCode(e.target.value)}
                placeholder="Nhập mã đơn hàng (VD: ORD-2026-XXXXX)"
                className="w-full pl-9 pr-3 py-2 bg-gray-50 border border-gray-300 rounded-lg text-xs text-gray-900 uppercase focus:outline-none focus:border-gray-900 focus:bg-white font-mono"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2 bg-gray-950 hover:bg-black text-white text-xs font-semibold rounded-lg transition"
            >
              {loading ? 'Đang tìm...' : 'Tra Cứu'}
            </button>
          </form>

          {errorMsg && (
            <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs">
              {errorMsg}
            </div>
          )}

          {order && (
            <div className="p-5 rounded-xl bg-gray-50 border border-gray-200 space-y-4">
              <div className="flex justify-between items-start border-b border-gray-200 pb-3">
                <div>
                  <span className="text-[10px] text-gray-500 font-semibold uppercase">Mã đơn hàng:</span>
                  <div className="text-sm font-bold text-gray-950 font-mono mt-0.5">{order.order_code}</div>
                  <div className="text-[11px] text-gray-500 mt-0.5">Thời gian tạo: {order.created_at}</div>
                </div>
                <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
                  {order.order_status === 'PROCESSING' ? 'Đang đóng gói chống sốc' : order.order_status}
                </span>
              </div>

              {/* Progress Steps (Text Only - No decorative icons) */}
              <div className="grid grid-cols-4 gap-1 text-center py-2 border-b border-gray-200 text-[10px]">
                <div className="font-bold text-emerald-800 border-t-2 border-emerald-700 pt-1">
                  1. Đã tiếp nhận
                </div>
                <div className="font-bold text-emerald-800 border-t-2 border-emerald-700 pt-1">
                  2. Đóng gói seal
                </div>
                <div className="font-medium text-gray-400 border-t-2 border-gray-300 pt-1">
                  3. Đang giao hàng
                </div>
                <div className="font-medium text-gray-400 border-t-2 border-gray-300 pt-1">
                  4. Hoàn tất
                </div>
              </div>

              <div className="text-xs space-y-1 text-gray-700">
                <p>Khách hàng: <strong className="text-gray-950">{order.customer_name}</strong></p>
                <p>Số điện thoại: <strong className="text-gray-950">{order.customer_phone}</strong></p>
                <p>Địa chỉ nhận: <strong className="text-gray-950">{order.shipping_address}</strong></p>
                <p>Phương thức: <strong className="text-gray-950">{order.payment_method}</strong></p>
              </div>

              {/* Items List */}
              <div className="border-t border-gray-200 pt-3 space-y-2">
                <span className="text-[11px] font-bold text-gray-900 uppercase">Sản Phẩm Trong Đơn</span>
                <div className="space-y-1.5">
                  {order.items?.map((it, idx) => (
                    <div key={idx} className="flex justify-between items-center text-xs py-1 border-b border-gray-100 last:border-0">
                      <div>
                        <div className="font-semibold text-gray-900">{it.product_title}</div>
                        <div className="text-[10px] text-gray-500">Số lượng: {it.quantity}</div>
                      </div>
                      <div className="font-bold text-gray-950">{formatCurrency(it.subtotal)}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex justify-between items-center pt-2 border-t border-gray-200">
                <span className="text-xs text-gray-600">Tổng thanh toán:</span>
                <span className="text-base font-bold text-gray-950">{formatCurrency(order.final_amount)}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
