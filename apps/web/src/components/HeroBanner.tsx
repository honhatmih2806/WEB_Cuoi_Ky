'use client';

import React from 'react';

interface HeroBannerProps {
  onOpenAdvisor: () => void;
  onExploreCategory: (categorySlug: string) => void;
}

export const HeroBanner: React.FC<HeroBannerProps> = ({
  onOpenAdvisor,
  onExploreCategory,
}) => {
  return (
    <div className="relative overflow-hidden rounded-2xl bg-[#F8F9FA] border border-gray-200 p-6 sm:p-12 mb-10 transition-all">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
        {/* Left Column: Editorial Headline & Value Propositions */}
        <div className="lg:col-span-7 space-y-6">
          <div className="inline-block px-3 py-1 bg-white border border-gray-200 text-gray-700 text-[11px] font-semibold tracking-wider uppercase rounded">
            Bộ Sưu Tập Thiết Bị Điện Tử Đầu Bảng 2026
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold text-gray-950 tracking-tight leading-[1.15]">
            Đỉnh Cao Công Nghệ.{' '}
            <span className="text-gray-500 font-normal">Chuẩn Mực Tinh Tế.</span>
          </h1>

          <p className="text-sm sm:text-base text-gray-600 leading-relaxed max-w-2xl font-normal">
            Tuyển tập những siêu phẩm phần cứng công nghệ từ các tập đoàn hàng đầu thế giới: Apple, NVIDIA, Sony, Dell, Samsung và Bang & Olufsen. Mọi thiết bị đều được kiểm định chất lượng nghiêm ngặt, phân phối chính hãng và hỗ trợ kỹ thuật chuyên sâu.
          </p>

          {/* 4 Pillars: Pure Typography - No icons describing content */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
            <div className="bg-white border border-gray-200 p-3.5 rounded-lg">
              <span className="text-[10px] font-bold text-gray-400 block tracking-wider">01. NGUỒN GỐC</span>
              <strong className="text-xs font-bold text-gray-900 block mt-1">100% Chính Hãng</strong>
              <p className="text-[11px] text-gray-500 mt-0.5">CO, CQ & VAT đầy đủ</p>
            </div>
            <div className="bg-white border border-gray-200 p-3.5 rounded-lg">
              <span className="text-[10px] font-bold text-gray-400 block tracking-wider">02. BẢO HÀNH</span>
              <strong className="text-xs font-bold text-gray-900 block mt-1">1 Đổi 1 Trong 30 Ngày</strong>
              <p className="text-[11px] text-gray-500 mt-0.5">Bảo hành 24 tháng</p>
            </div>
            <div className="bg-white border border-gray-200 p-3.5 rounded-lg">
              <span className="text-[10px] font-bold text-gray-400 block tracking-wider">03. VẬN CHUYỂN</span>
              <strong className="text-xs font-bold text-gray-900 block mt-1">Giao Hỏa Tốc 2H</strong>
              <p className="text-[11px] text-gray-500 mt-0.5">Đóng gói chuẩn chống sốc</p>
            </div>
            <div className="bg-white border border-gray-200 p-3.5 rounded-lg">
              <span className="text-[10px] font-bold text-gray-400 block tracking-wider">04. KỸ THUẬT</span>
              <strong className="text-xs font-bold text-gray-900 block mt-1">Chuyên Gia Tư Vấn</strong>
              <p className="text-[11px] text-gray-500 mt-0.5">Tối ưu AI & Đồ họa</p>
            </div>
          </div>

          {/* Action CTAs */}
          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              onClick={() => onExploreCategory('all')}
              className="px-6 py-3 bg-gray-950 hover:bg-black text-white text-xs font-semibold rounded-lg transition-colors"
            >
              Khám Phá Toàn Bộ Sản Phẩm
            </button>
            <button
              onClick={onOpenAdvisor}
              className="px-5 py-3 bg-white hover:bg-gray-100 text-gray-900 border border-gray-300 text-xs font-semibold rounded-lg transition-colors"
            >
              Tư Vấn Cấu Hình Phù Hợp
            </button>
          </div>
        </div>

        {/* Right Column: Clean Editorial Product Showcase */}
        <div className="lg:col-span-5">
          <div className="bg-white border border-gray-200 rounded-xl p-4 sm:p-5 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3 text-xs">
              <span className="font-semibold text-gray-900">SẢN PHẨM TIÊU BIỂU TRONG TUẦN</span>
              <span className="text-[10px] font-bold px-2 py-0.5 bg-gray-100 text-gray-700 rounded">
                FLAGSHIP 2026
              </span>
            </div>

            <div className="relative aspect-[4/3] rounded-lg overflow-hidden bg-gray-50 border border-gray-100">
              <img
                src="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80"
                alt="MacBook Pro & High-End Tech"
                className="w-full h-full object-cover"
              />
            </div>

            <div className="flex items-center justify-between pt-1">
              <div>
                <p className="text-[11px] text-gray-500 uppercase tracking-wider font-medium">Apple & NVIDIA Ecosystem</p>
                <h4 className="text-sm font-bold text-gray-950 mt-0.5">MacBook Pro 16" M4 Max & RTX 5090</h4>
              </div>
              <button
                onClick={() => onExploreCategory('laptops')}
                className="text-xs font-semibold text-gray-900 underline underline-offset-4 hover:text-black transition"
              >
                Xem chi tiết
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
