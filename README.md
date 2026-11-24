# UteTechStore — Nền Tảng Thương Mại Điện Tử Thiết Bị Công Nghệ Cao Cấp

[![Next.js 14](https://img.shields.io/badge/Next.js-14%20App%20Router-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.165+-green.svg)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4+-38bdf8.svg)](https://tailwindcss.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4+-blue.svg)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-yellow.svg)](https://python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20Postgres-indigo.svg)](https://sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Active%20Development-emerald.svg)]()

> **UteTechStore** là nền tảng thương mại điện tử cao cấp chuyên phân phối các thiết bị điện tử, máy tính xách tay, điện thoại flagship, thiết bị âm thanh Hi-Fi, màn hình đồ họa chuyên nghiệp và linh kiện máy tính hàng đầu. Dự án được xây dựng với ngôn ngữ thiết kế tối giản, tươi sáng, sang trọng và thanh lịch, mang lại trải nghiệm mua sắm trực tuyến vượt trội.

---

## 🌐 Đường Dẫn Truy Cập Trực Tiếp (Local & Live)

* **Cửa Hàng Trực Tuyến (Next.js 14):** [http://localhost:3000](http://localhost:3000)
* **Tài Liệu Backend API (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Kiểm Tra Trạng Thái Hệ Thống:** [http://localhost:8000/health](http://localhost:8000/health)

---

## ⚡ Khởi Chạy 1-Click (Dành Cho Windows)

Chỉ cần nhấp đúp vào một trong hai tệp lệnh ngay tại thư mục gốc:
👉 **`start.bat`** hoặc **`run_store.bat`**

Hệ thống sẽ tự động kích hoạt đồng thời cả Backend FastAPI (`:8000`) và Frontend Next.js (`:3000`), sau đó tự động mở trình duyệt web.

---

## 🌟 Điểm Nhấn Kiến Trúc & Tính Năng Nổi Bật

### 1. Thiết Kế Tươi Sáng & Sang Trọng (Luxury Minimalist)
* **Bảng màu:** Nền trắng tinh khiết (`#FFFFFF`), bề mặt xám nhạt trung tính (`#F8F9FA`), đường viền hairline siêu mảnh (`#E5E7EB`), chữ đen than trầm có độ tương phản cao (`#0F172A`).
* **Không dùng icon để miêu tả nội dung:** Toàn bộ cam kết dịch vụ, danh mục sản phẩm và thông số kỹ thuật được cấu trúc bằng số thứ tự La Tinh (`01.`, `02.`), typography thanh lịch và hệ thống phân cấp văn bản rõ ràng.

### 2. Danh Mục Thiết Bị Điện Tử Toàn Diện
* **Máy Tính Xách Tay (Laptops & MacBooks):** Apple MacBook Pro M4 Max, MacBook Air M3, Dell XPS 16, Lenovo ThinkPad X1 Carbon Gen 12, ASUS ROG Zephyrus G16.
* **Điện Thoại Flagship:** iPhone 16 Pro Max, Samsung Galaxy S24 Ultra, Google Pixel 9 Pro XL, Sony Xperia 1 VI.
* **Máy Tính Bảng (Tablets & iPads):** iPad Pro 13" M4 Ultra Retina Tandem OLED, Samsung Galaxy Tab S9 Ultra.
* **Âm Thanh & Tai Nghe Hi-Fi:** AirPods Max, Sony WH-1000XM5, Bang & Olufsen Beoplay H95.
* **Màn Hình Chuyên Nghiệp:** Apple Studio Display 5K, Dell UltraSharp 32" 6K, LG UltraGear OLED 4K.
* **Linh Kiện Máy Tính & Đồ Họa:** NVIDIA GeForce RTX 5090 32GB, RTX 4090 24GB.
* **Thiết Bị Đeo & Phụ Kiện:** Apple Watch Ultra 2, Bàn phím cơ nhôm Keychron Q1 Max, Chuột công thái học Logitech MX Master 3S.

### 3. Quy Trình Mua Sắm & Thanh Toán Hiện Đại
* Giỏ hàng thời gian thực, hỗ trợ mã ưu đãi: `UTEVIP` (giảm 5%), `LUXURY` (giảm 10%), `UTETECHSTORE` (giảm 1.000.000₫).
* Thanh toán tự động **VietQR chuẩn ngân hàng** (tạo mã QR động kèm đúng số tiền và cú pháp đơn hàng) cùng hình thức COD đồng kiểm khi nhận hàng.
* Tra cứu trạng thái đơn hàng tức thì theo mã vận đơn (`ORD-2026-XXXXX`) với thanh tiến trình trực quan.
* Trợ lý tư vấn cấu hình phần cứng thông minh đề xuất thiết bị theo nhu cầu thực tế.
* Cơ chế **Fallback Zero-Downtime**: Tích hợp sẵn bộ dữ liệu offline giúp trang web luôn hiển thị mượt mà kể cả khi backend đang bảo trì.

---

## 👥 Phân Công Nhiệm Vụ Thành Viên

Dự án đã soạn thảo chi tiết 2 tệp nhiệm vụ kỹ thuật tại thư mục gốc:

| Thành Viên | Trách Nhiệm Chính | Tệp Hướng Dẫn Kỹ Thuật |
| :--- | :--- | :--- |
| **Thành viên 1** | Tinh chỉnh & chuẩn hóa dữ liệu sản phẩm (Ít chữ, súc tích, sang trọng chuẩn boutique) | [NHIEM_VU_THANH_VIEN_1_DATA_SAN_PHAM.md](./NHIEM_VU_THANH_VIEN_1_DATA_SAN_PHAM.md) |
| **Thành viên 2** | Xây dựng công cụ định giá sản phẩm (Trade-in) & Hoàn thiện Backend tìm kiếm theo tên / khoảng giá | [NHIEM_VU_THANH_VIEN_2_DINH_GIA_VA_TIM_KIEM.md](./NHIEM_VU_THANH_VIEN_2_DINH_GIA_VA_TIM_KIEM.md) |

---

## 📁 Cấu Trúc Mã Nguồn

```
.
├── apps/
│   ├── api/                  # Backend FastAPI (Python 3.12)
│   │   ├── core/             # Cấu hình hệ thống, kết nối Database, Security, Exceptions
│   │   ├── models/           # SQLAlchemy Entities (Product, Brand, Category, Order, Specs)
│   │   ├── routers/          # API Controllers (products, categories, orders, advisor)
│   │   ├── schemas/          # Pydantic DTOs cho Request/Response
│   │   └── main.py           # Điểm khởi chạy FastAPI app
│   └── web/                  # Frontend Next.js 14 (App Router, Tailwind CSS)
│       ├── src/
│       │   ├── app/          # App Router, globals.css, layout.tsx, page.tsx
│       │   ├── components/   # Navbar, HeroBanner, ProductCard, DetailModal, Cart, Checkout...
│       │   ├── services/     # API Client & Fallback Data Module
│       │   └── types/        # TypeScript DTOs
├── scripts/
│   ├── seed_products.py      # Script nạp dữ liệu sản phẩm vào CSDL SQLite
│   └── start_servers.py      # Script chạy nền đồng thời cả Backend và Frontend
├── start.bat                 # File khởi chạy 1-click cho Windows
├── run_store.bat             # File khởi chạy nhanh cho Windows
├── start.sh                  # Kịch bản khởi chạy cho Linux / macOS / Git Bash
├── dev.sh                    # Kịch bản phát triển cho Backend
├── titan_silicon.db          # Cơ sở dữ liệu SQLite đã được nạp dữ liệu đầy đủ
├── NHIEM_VU_THANH_VIEN_1_DATA_SAN_PHAM.md
├── NHIEM_VU_THANH_VIEN_2_DINH_GIA_VA_TIM_KIEM.md
└── README.md
```

---

## 🛠️ Hướng Dẫn Cài Đặt Cho Thành Viên Mới

### 1. Clone Kho Mã Nguồn:
```bash
git clone https://github.com/honhatmih2806/WEB_Cuoi_Ky.git
cd WEB_Cuoi_Ky
```

### 2. Khởi Chạy Nhanh:
- **Trên Windows:** Nhấp đúp vào `start.bat`.
- **Trên Linux / macOS / Git Bash:**
  ```bash
  chmod +x start.sh dev.sh
  ./start.sh
  ```

---
© 2026 UteTechStore • Nền tảng thương mại điện tử công nghệ cao cấp.
