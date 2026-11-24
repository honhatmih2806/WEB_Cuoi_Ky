'use client';

import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-20 border-t border-gray-200 bg-gray-50 text-gray-600 text-xs">
      {/* 4 Feature Pillars (Text Only - No decorative icons describing content) */}
      <div className="border-b border-gray-200 py-10 px-4">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="space-y-1.5 p-4 bg-white border border-gray-200 rounded-lg">
            <span className="text-[10px] font-bold text-gray-400 block tracking-wider uppercase">01. CAM KẾT XUẤT XỨ</span>
            <h4 className="font-bold text-gray-950 text-sm">100% Chính Hãng Phân Phối</h4>
            <p className="text-gray-500 text-xs leading-relaxed">
              Nhập khẩu chính ngạch trực tiếp từ Apple, NVIDIA, Sony, Dell, Samsung với đầy đủ CO/CQ và hóa đơn VAT.
            </p>
          </div>

          <div className="space-y-1.5 p-4 bg-white border border-gray-200 rounded-lg">
            <span className="text-[10px] font-bold text-gray-400 block tracking-wider uppercase">02. TIÊU CHUẨN BẢO HÀNH</span>
            <h4 className="font-bold text-gray-950 text-sm">Bảo Hành 1 Đổi 1 Tận Nơi</h4>
            <p className="text-gray-500 text-xs leading-relaxed">
              Thời hạn bảo hành 12 đến 24 tháng theo tiêu chuẩn toàn cầu, hỗ trợ đổi mới thiết bị trong 30 ngày đầu.
            </p>
          </div>

          <div className="space-y-1.5 p-4 bg-white border border-gray-200 rounded-lg">
            <span className="text-[10px] font-bold text-gray-400 block tracking-wider uppercase">03. VẬN CHUYỂN BẢO HIỂM</span>
            <h4 className="font-bold text-gray-950 text-sm">Giao Hỏa Tốc & Đồng Kiểm</h4>
            <p className="text-gray-500 text-xs leading-relaxed">
              Đóng thùng chống sốc 3 lớp, giao hàng trong 2 giờ tại nội thành và miễn phí vận chuyển bảo hiểm toàn quốc.
            </p>
          </div>

          <div className="space-y-1.5 p-4 bg-white border border-gray-200 rounded-lg">
            <span className="text-[10px] font-bold text-gray-400 block tracking-wider uppercase">04. HỖ TRỢ KỸ THUẬT</span>
            <h4 className="font-bold text-gray-950 text-sm">Chuyên Gia Tư Vấn 24/7</h4>
            <p className="text-gray-500 text-xs leading-relaxed">
              Đội ngũ kỹ sư phần cứng giàu kinh nghiệm hỗ trợ cài đặt môi trường AI, dựng phim 4K và benchmark phần mềm.
            </p>
          </div>
        </div>
      </div>

      {/* Main Corporate Information & Policies */}
      <div className="max-w-7xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-12 gap-8">
        <div className="md:col-span-5 space-y-3">
          <div className="flex items-center gap-2">
            <span className="w-7 h-7 rounded bg-gray-950 text-white font-black text-xs flex items-center justify-center">
              TS
            </span>
            <span className="text-sm font-bold text-gray-950 tracking-tight">
              TECH STORE 合同会社 (JAPAN & VIETNAM)
            </span>
          </div>

          <p className="text-gray-500 leading-relaxed text-xs max-w-md">
            Hệ sinh thái bán lẻ thiết bị điện tử và giải pháp điện toán công nghệ cao cấp. Chúng tôi tập trung vào trải nghiệm phần cứng đỉnh cao từ các thương hiệu công nghệ danh tiếng nhất thế giới.
          </p>

          <div className="space-y-1 text-[11px] text-gray-500 pt-1">
            <p><strong>Mã số doanh nghiệp Nhật Bản:</strong> 9030003019539</p>
            <p><strong>Giấy phép kinh doanh Việt Nam:</strong> 0109887766 do Sở KH&ĐT TP.HCM cấp</p>
            <p><strong>Trụ sở chính:</strong> 3-13-11 Chuo, Moroyama-machi, Iruma-gun, Saitama 350-0461, Japan</p>
          </div>
        </div>

        {/* Flagship Showrooms */}
        <div className="md:col-span-4 space-y-2 text-xs">
          <h4 className="font-bold text-gray-950 uppercase tracking-wider text-[11px]">
            Hệ Thống Flagship Showroom
          </h4>
          <div className="space-y-2 text-gray-600">
            <div>
              <strong className="text-gray-900 block">Showroom TP. Hồ Chí Minh:</strong>
              <span>Tòa nhà Bitexco Financial Tower, 2 Hải Triều, P. Bến Nghé, Quận 1</span>
            </div>
            <div>
              <strong className="text-gray-900 block">Showroom Hà Nội:</strong>
              <span>18 Phố Huế, Phường Hàng Bài, Quận Hoàn Kiếm</span>
            </div>
            <div>
              <strong className="text-gray-900 block">Showroom Đà Nẵng:</strong>
              <span>56 Nguyễn Văn Linh, Phường Nam Dương, Quận Hải Châu</span>
            </div>
          </div>
        </div>

        {/* Policies and Quick Links */}
        <div className="md:col-span-3 space-y-2 text-xs">
          <h4 className="font-bold text-gray-950 uppercase tracking-wider text-[11px]">
            Chính Sách & Quy Định
          </h4>
          <ul className="space-y-1.5 text-gray-600">
            <li>
              <a href="#terms" className="hover:text-black transition">Điều khoản & Điều kiện sử dụng</a>
            </li>
            <li>
              <a href="#privacy" className="hover:text-black transition">Chính sách bảo mật thông tin</a>
            </li>
            <li>
              <a href="#shipping" className="hover:text-black transition">Quy định vận chuyển & Giao nhận</a>
            </li>
            <li>
              <a href="#return" className="hover:text-black transition">Chính sách bảo hành & Đổi trả 30 ngày</a>
            </li>
            <li>
              <a href="#about" className="hover:text-black transition">Giới thiệu TECH STORE Flagship</a>
            </li>
          </ul>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-200 py-6 px-4 bg-white text-[11px] text-gray-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-3">
          <div>
            © 2026 TECH STORE 合同会社 • Tất cả quyền được bảo lưu.
          </div>
          <div className="flex items-center gap-3 text-gray-600 font-medium">
            <span>Phương thức thanh toán hỗ trợ:</span>
            <span className="text-gray-950 font-semibold">VietQR</span>
            <span>•</span>
            <span className="text-gray-950 font-semibold">Visa / Mastercard</span>
            <span>•</span>
            <span className="text-gray-950 font-semibold">COD Đồng Kiểm</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
