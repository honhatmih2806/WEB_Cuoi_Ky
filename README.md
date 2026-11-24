# TECH STORE — Japanese Luxury Electronics & Computing Flagship Platform

[![Next.js 14](https://img.shields.io/badge/Next.js-14%20App%20Router-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.165+-green.svg)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4+-38bdf8.svg)](https://tailwindcss.com/)
[![SQLite / PostgreSQL](https://img.shields.io/badge/Database-SQLite%20%7C%20Postgres-blue.svg)](https://sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Online%20%26%20Deployed-emerald.svg)]()

> **TECH STORE (TECH STORE 合同会社)** là nền tảng thương mại điện tử chuyên nghiệp cung cấp đầy đủ các thiết bị điện tử, máy tính xách tay, điện thoại flagship, thiết bị âm thanh Hi-Fi, máy chơi game và phần cứng AI đầu bảng. Lấy cảm hứng từ triết lý thẩm mỹ tối giản, tươi sáng và sang trọng của các boutique công nghệ Nhật Bản (tham khảo [techstore.jp](https://techstore.jp/)).

---

## 🌐 Đường Dẫn Truy Cập Trực Tiếp (Live Deployment)

* **Trang Web Public Trên Internet:** [https://techstore-japan-2026.loca.lt](https://techstore-japan-2026.loca.lt)  
  *(Nếu màn hình Tunnel hiển thị yêu cầu Tunnel Password lần đầu, nhập IP máy chủ: `42.113.216.225`)*
* **Cửa Hàng Local:** [http://localhost:3000](http://localhost:3000)
* **Tài Liệu API Backend (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **API Kiểm Tra Sức Khỏe:** [http://localhost:8000/health](http://localhost:8000/health)

---

## ⚡ Khởi Chạy 1-Click (Dành cho Windows)

Chỉ cần nhấp đúp vào tệp:
👉 **`run_store.bat`** (nằm ngay tại thư mục gốc dự án)

Hệ thống sẽ tự động kích hoạt cả Backend FastAPI (`:8000`) và Frontend Next.js (`:3000`), sau đó tự động mở trình duyệt.

---

## 🌟 Điểm Nhấn Thiết Kế & Tính Năng Độc Quyền

1. **Thẩm Mỹ Tươi Sáng & Chuẩn Luxury Nhật Bản (techstore.jp):**
   * Tông màu chủ đạo: Nền trắng tinh khiết (`#FFFFFF`), bề mặt xám nhạt trung tính (`#F8F9FA`), viền hairline siêu mảnh (`#E5E7EB`), chữ đen than trầm có độ tương phản cao (`#0F172A`).
   * **Không dùng icon để miêu tả nội dung:** Toàn bộ thông điệp cam kết, danh mục và thông số kỹ thuật được cấu trúc bằng chữ số la tinh (`01.`, `02.`), typography DM Sans thanh lịch và hệ thống phân cấp văn bản chuyên nghiệp.
2. **Danh Mục 29 Thiết Bị Điện Tử Hàng Đầu:**
   * **Laptops:** MacBook Pro 16" M4 Max, MacBook Air 15" M3, Dell XPS 16 9640 4K+ OLED, ASUS ROG Zephyrus G16, Lenovo ThinkPad X1 Carbon Gen 12.
   * **Smartphones:** iPhone 16 Pro Max 1TB Titan Sa Mạc, Samsung Galaxy S24 Ultra 512GB, Google Pixel 9 Pro XL, Sony Xperia 1 VI.
   * **Tablets:** iPad Pro 13" M4 Ultra Retina Tandem OLED 5.1mm, Samsung Galaxy Tab S9 Ultra 14.6".
   * **Audio & Hi-Fi:** AirPods Max USB-C 2026, Sony WH-1000XM5 Hi-Res LDAC, Bang & Olufsen Beoplay H95 Nordic Ice Titanium.
   * **Monitors:** Apple Studio Display 27" 5K Nano-Texture, Dell UltraSharp 32" 6K IPS Black, LG UltraGear 32" 4K OLED 240Hz/480Hz.
   * **PC & AI Hardware:** NVIDIA GeForce RTX 5090 FE 32GB GDDR7, RTX 4090 24GB, Jetson AGX Orin 64GB 275 TOPS.
   * **Gaming Consoles:** Sony PlayStation 5 Pro 2TB PSSR, Nintendo Switch OLED Mario Red.
   * **Wearables & Accessories:** Apple Watch Ultra 2 Titanium 49mm, Galaxy Watch Ultra 47mm LTE, Cáp Thunderbolt 5 Pro 2m 120Gbps, Bàn phím nhôm CNC Keychron Q1 Max, Chuột Logitech MX Master 3S.
3. **Quy Trình Mua Sắm & Thanh Toán Hiện Đại:**
   * Giỏ hàng thời gian thực, hỗ trợ mã giảm giá `TITANVIP` (giảm 5%), `LUXURY` (giảm 10%).
   * Thanh toán chuyển khoản tự động **VietQR chuẩn ngân hàng** (tạo mã QR trực tiếp kèm đúng số tiền và nội dung đơn) hoặc COD đồng kiểm.
   * Tra cứu đơn hàng theo mã vận đơn tức thì (`ORD-2026-XXXXX`) với thanh tiến trình 4 giai đoạn.
   * Trợ lý tư vấn cấu hình phần cứng thông minh tự động đề xuất combo theo nhu cầu kỹ thuật (AI/LLM, Cinema 4K, Gaming, Robotics).
4. **Cơ Chế Fallback Zero-Downtime:**
   * Tích hợp kho dữ liệu fallback hoàn chỉnh trong frontend. Trang web hoạt động mượt mà và hiển thị dữ liệu đầy đủ ngay cả khi chạy độc lập không phụ thuộc backend.

---

## 📁 Cấu Trúc Mã Nguồn

```
.
├── apps/
│   ├── api/                  # FastAPI Backend (Python 3.12)
│   │   ├── core/             # Database connection, config, exceptions
│   │   ├── models/           # SQLAlchemy Entities (Product, Brand, Category, Order, Specs)
│   │   ├── routers/          # Controllers (products, categories, orders, advisor)
│   │   └── main.py           # FastAPI entry point
│   └── web/                  # Next.js 14 Frontend (App Router, Tailwind CSS)
│       ├── src/
│       │   ├── app/          # App router, globals.css, layout.tsx, page.tsx
│       │   ├── components/   # Navbar, HeroBanner, ProductCard, DetailModal, Cart, Checkout...
│       │   ├── services/     # API Client & Fallback Data Module
│       │   └── types/        # TypeScript DTOs
├── scripts/
│   ├── seed_products.py      # Script nạp 29 sản phẩm điện tử cao cấp vào CSDL
│   └── start_servers.py      # Script chạy nền đồng thời cả Backend và Frontend
├── run_store.bat             # File khởi chạy 1-click cho Windows
├── titan_silicon.db          # Cơ sở dữ liệu SQLite đã được nạp dữ liệu đầy đủ
└── README.md
```
