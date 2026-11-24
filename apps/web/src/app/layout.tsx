import React from 'react';
import './globals.css';

export const metadata = {
  title: 'UteTechStore — Siêu Thị Thiết Bị Điện Tử & Công Nghệ Cao Cấp',
  description:
    'Nền tảng thương mại điện tử chuyên nghiệp cung cấp đầy đủ các sản phẩm điện tử chính hãng từ Apple, NVIDIA, Sony, Dell, Samsung: Laptops, Smartphones, Tablets, Âm thanh Hi-Fi, Màn hình đồ họa, Máy chơi game và Phụ kiện cao cấp.',
  keywords: 'UteTechStore, UTE Tech Store, MacBook Pro M4, iPhone 16 Pro Max, NVIDIA RTX 5090, Sony WH-1000XM5, Dell XPS, Thiết bị điện tử chính hãng',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <body className="bg-white text-gray-950 min-h-screen antialiased selection:bg-gray-950 selection:text-white">
        {children}
      </body>
    </html>
  );
}
