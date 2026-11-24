'use client';

import React, { useState } from 'react';
import { X } from 'lucide-react';
import { AdvisorRecommendation, Product } from '../types';
import { formatCurrency } from './ProductCard';
import { getAdvisorRecommendation } from '../services/api';

interface SynergyAdvisorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAddProductToCart: (product: Product) => void;
}

export const SynergyAdvisorModal: React.FC<SynergyAdvisorModalProps> = ({
  isOpen,
  onClose,
  onAddProductToCart,
}) => {
  const [useCase, setUseCase] = useState<string>('DEEP_LEARNING');
  const [budget, setBudget] = useState<string>('HIGH');
  const [loading, setLoading] = useState<boolean>(false);
  const [recommendation, setRecommendation] = useState<AdvisorRecommendation | null>(null);

  if (!isOpen) return null;

  const handleGenerate = async () => {
    setLoading(true);
    const res = await getAdvisorRecommendation({
      use_case: useCase,
      budget_range: budget,
      primary_focus: 'BOTH',
    });
    setLoading(false);
    if (res) {
      setRecommendation(res);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/40 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-3xl bg-white border border-gray-200 rounded-2xl shadow-xl overflow-hidden my-auto max-h-[92vh] flex flex-col">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-gray-200 flex items-center justify-between bg-gray-50">
          <div>
            <h2 className="text-sm sm:text-base font-bold text-gray-950 uppercase tracking-wide">
              Hệ Thống Tư Vấn Cấu Hình Chuyên Nghiệp
            </h2>
            <p className="text-[11px] text-gray-500">
              Phân tích yêu cầu kỹ thuật và đề xuất giải pháp phần cứng tối ưu
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

        {/* Modal Content */}
        <div className="p-5 sm:p-7 overflow-y-auto space-y-6 flex-1">
          {/* Question 1: Use Case (Text Only - No decorative icons) */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-900 uppercase tracking-wider block">
              1. Mục đích công việc & nhu cầu kỹ thuật chính:
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {[
                {
                  id: 'DEEP_LEARNING',
                  title: 'Trí Tuệ Nhân Tạo & Huấn Luyện LLM',
                  desc: 'Chạy LLaMA-3, Stable Diffusion, tinh chỉnh model, giám sát máy trạm từ xa',
                },
                {
                  id: '4K_PRORES_CINEMA',
                  title: 'Dựng Phim 4K120fps & Đồ Họa Studio',
                  desc: 'Ghi hình Apple Log, dựng DaVinci/Premiere, xuất file siêu tốc với Dual NVENC',
                },
                {
                  id: 'GAMING_STREAMING',
                  title: 'Gaming 4K Ray Tracing & Livestream',
                  desc: 'Max Settings Path Tracing, DLSS 3.5 và biến iPhone thành Studio Facecam 4K',
                },
                {
                  id: 'MOBILE_EDGE_AI',
                  title: 'Thị Giác Máy Tính & Robotics SLAM',
                  desc: 'Thu thập LiDAR Scanner từ iPhone và xử lý biên thời gian thực qua Jetson Orin',
                },
              ].map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setUseCase(item.id)}
                  className={`p-3 rounded-xl border text-left transition ${
                    useCase === item.id
                      ? 'border-gray-950 bg-gray-50 font-semibold'
                      : 'border-gray-200 hover:border-gray-400 bg-white'
                  }`}
                >
                  <div className="text-xs font-bold text-gray-950">{item.title}</div>
                  <div className="text-[11px] text-gray-500 mt-0.5 leading-snug">{item.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Question 2: Budget */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-900 uppercase tracking-wider block">
              2. Khoảng ngân sách đầu tư dự kiến:
            </label>
            <div className="grid grid-cols-3 gap-2.5">
              {[
                { id: 'MID', title: 'Dưới 50 Triệu', desc: 'Tối ưu chi phí / hiệu năng' },
                { id: 'HIGH', title: '50 - 100 Triệu', desc: 'Tiêu chuẩn Studio cao cấp' },
                { id: 'FLAGSHIP', title: 'Trên 100 Triệu', desc: 'Cấu hình đỉnh cao tuyệt đối' },
              ].map((b) => (
                <button
                  key={b.id}
                  type="button"
                  onClick={() => setBudget(b.id)}
                  className={`p-3 rounded-xl border text-center transition ${
                    budget === b.id
                      ? 'border-gray-950 bg-gray-50 font-semibold'
                      : 'border-gray-200 hover:border-gray-400 bg-white'
                  }`}
                >
                  <div className="text-xs font-bold text-gray-950">{b.title}</div>
                  <div className="text-[10px] text-gray-500 mt-0.5">{b.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Generate Button */}
          <div>
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="w-full py-3 bg-gray-950 hover:bg-black text-white text-xs font-semibold rounded-lg shadow-sm transition disabled:opacity-50"
            >
              {loading ? 'Hệ thống đang tính toán...' : 'Phân Tích & Đề Xuất Cấu Hình Tối Ưu'}
            </button>
          </div>

          {/* Recommendation Result */}
          {recommendation && (
            <div className="mt-6 p-5 sm:p-6 rounded-xl border border-gray-200 bg-gray-50 space-y-5">
              <div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200 uppercase tracking-wider">
                  Cấu Hình Khuyến Nghị Chuẩn
                </span>
                <h3 className="text-base font-bold text-gray-950 mt-1.5">
                  {recommendation.title}
                </h3>
                <p className="text-xs text-gray-600 mt-0.5">{recommendation.subtitle}</p>
              </div>

              {/* Matched Products */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {recommendation.matched_iphone && (
                  <div className="p-3.5 rounded-lg border border-gray-200 bg-white space-y-2">
                    <div className="text-[10px] font-bold text-gray-500 uppercase">
                      Thiết Bị Di Động
                    </div>
                    <div className="text-xs font-bold text-gray-950">
                      {recommendation.matched_iphone.title}
                    </div>
                    <div className="text-xs text-gray-950 font-semibold">
                      {formatCurrency(recommendation.matched_iphone.price)}
                    </div>
                    <button
                      onClick={() => onAddProductToCart(recommendation.matched_iphone!)}
                      className="w-full py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-900 text-[11px] font-semibold rounded transition"
                    >
                      Thêm Vào Giỏ
                    </button>
                  </div>
                )}

                {recommendation.matched_nvidia && (
                  <div className="p-3.5 rounded-lg border border-gray-200 bg-white space-y-2">
                    <div className="text-[10px] font-bold text-gray-500 uppercase">
                      Xử Lý Đồ Họa & AI
                    </div>
                    <div className="text-xs font-bold text-gray-950">
                      {recommendation.matched_nvidia.title}
                    </div>
                    <div className="text-xs text-gray-950 font-semibold">
                      {formatCurrency(recommendation.matched_nvidia.price)}
                    </div>
                    <button
                      onClick={() => onAddProductToCart(recommendation.matched_nvidia!)}
                      className="w-full py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-900 text-[11px] font-semibold rounded transition"
                    >
                      Thêm Vào Giỏ
                    </button>
                  </div>
                )}
              </div>

              {/* Technical Reason */}
              <div className="p-3.5 rounded-lg border border-gray-200 bg-white text-xs space-y-1">
                <span className="font-bold text-gray-900">Cơ Sở Đánh Giá Kỹ Thuật:</span>
                <p className="text-gray-600 leading-relaxed">{recommendation.synergy_reason}</p>
              </div>

              {/* Benchmark Table (Text Only) */}
              {recommendation.benchmark_scores && (
                <div className="rounded-lg border border-gray-200 overflow-hidden bg-white text-xs">
                  <div className="p-2.5 bg-gray-100/70 font-bold text-gray-900 text-[11px] uppercase tracking-wider border-b border-gray-200">
                    Bảng Chỉ Số Hiệu Năng Dự Kiến
                  </div>
                  {Object.entries(recommendation.benchmark_scores).map(([k, v], idx) => (
                    <div
                      key={k}
                      className={`flex justify-between p-2.5 ${
                        idx % 2 === 0 ? 'bg-gray-50/50' : 'bg-white'
                      } border-b border-gray-100 last:border-0`}
                    >
                      <span className="font-medium text-gray-600">{k.replace(/_/g, ' ')}:</span>
                      <span className="font-bold text-gray-950">{String(v)}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
