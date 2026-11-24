# UteTechStore — Nền Tảng Thương Mại Điện Tử Thiết Bị Công Nghệ Cao Cấp

[![Next.js 14](https://img.shields.io/badge/Next.js-14%20App%20Router-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.165+-green.svg)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4+-38bdf8.svg)](https://tailwindcss.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4+-blue.svg)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-yellow.svg)](https://python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20Postgres-indigo.svg)](https://sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Active%20Development-emerald.svg)]()

> **UteTechStore** là nền tảng thương mại điện tử chuyên nghiệp cung cấp đầy đủ các thiết bị điện tử, máy tính xách tay, điện thoại flagship, thiết bị âm thanh Hi-Fi, màn hình đồ họa và linh kiện máy tính cao cấp. Dự án được xây dựng với ngôn ngữ thiết kế tối giản, tươi sáng và sang trọng, mang lại trải nghiệm mua sắm trực tuyến vượt trội.

---

## 🌐 Đường Dẫn Truy Cập Trực Tiếp (Local & Live)

* **Cửa Hàng Trực Tuyến (Next.js 14):** [http://localhost:3000](http://localhost:3000)
* **Tài Liệu Backend API (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Kiểm Tra Trạng Thái Hệ Thống:** [http://localhost:8000/health](http://localhost:8000/health)

---

## ⚡ Hướng Dẫn Khởi Chạy Nhanh (Quick Start)

Hệ thống đã chuẩn bị sẵn các kịch bản khởi động tự động cho từng loại Terminal / Hệ điều hành:

| Môi Trường / Terminal | Lệnh Thực Thi | Mô Tả |
| :--- | :--- | :--- |
| **Windows (1-Click UI)** | Nhấp đúp vào **`start.bat`** *(hoặc `run_store.bat`)* | Tự bật 2 cửa sổ Backend & Frontend, tự mở trình duyệt |
| **Windows PowerShell** | `.\start.ps1` | Script chuyên dụng cho PowerShell, tự cấu hình môi trường |
| **Mọi hệ điều hành (Python)** | `python scripts/start_servers.py` | Chạy đồng thời cả 2 server trên cùng 1 terminal |
| **Git Bash / Linux / macOS** | `./start.sh` *(hoặc `bash start.sh`)* | Tự nhận diện môi trường Docker / Local Native |

> [!NOTE]
> **Lưu ý quan trọng cho Windows:** Nếu bạn đang mở cửa sổ **PowerShell** (`PS C:\...`), hãy chạy **`.\start.ps1`** hoặc **`.\start.bat`**. Không gõ `./start.sh` vì PowerShell không hỗ trợ thực thi trực tiếp tệp shell script của Linux.

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

## 🛠️ Hướng Dẫn Cài Đặt Chi Tiết Cho Thành Viên Mới

### Bước 1: Kéo Kho Mã Nguồn Về Máy (Clone Repo)
```bash
git clone https://github.com/honhatmih2806/WEB_Cuoi_Ky.git
cd WEB_Cuoi_Ky
```

### Bước 2: Khởi Chạy Tự Động (Chọn 1 trong các cách sau)
- **Nếu dùng Windows (Khuyên dùng):**
  - Mở PowerShell và gõ:
    ```powershell
    .\start.ps1
    ```
  - Hoặc nhấp đúp vào file `start.bat`.
- **Nếu dùng Git Bash / Linux / macOS:**
  ```bash
  chmod +x start.sh dev.sh
  ./start.sh
  ```

---

### Bước 3: Khởi Chạy Thủ Công Từng Phần (Dành Khi Lập Trình & Debug)

#### 🔹 1. Khởi động Backend (FastAPI):
Mở một cửa sổ terminal tại thư mục dự án:
```powershell
# Tạo và kích hoạt môi trường ảo Python
python -m venv .venv

# Kích hoạt trên Windows:
.\.venv\Scripts\activate
# (Hoặc trên Mac/Linux: source .venv/bin/activate)

# Cài đặt thư viện
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-multipart email-validator passlib python-jose httpx requests scikit-learn numpy

# Khởi chạy server API
cd apps/api
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
> API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

#### 🔹 2. Khởi động Frontend (Next.js 14):
Mở một cửa sổ terminal thứ hai:
```powershell
cd apps/web

# Cài đặt node_modules
npm install

# Khởi chạy frontend
npm run dev
```
> Web Store: [http://localhost:3000](http://localhost:3000)

---

## 🔀 Quy Trình Phối Hợp Làm Việc Trên Git (Team Git Workflow)

1. **Tạo nhánh làm việc riêng (Không sửa trực tiếp trên `main`):**
   ```bash
   git checkout -b feature/<ten-tinh-nang>
   # Ví dụ TV1: git checkout -b feature/refine-product-data
   # Ví dụ TV2: git checkout -b feature/pricing-and-search
   ```
2. **Thực hiện code và kiểm thử chạy mượt mà trên máy local.**
3. **Commit và đẩy nhánh lên GitHub:**
   ```bash
   git add .
   git commit -m "feat: mô tả công việc đã làm"
   git push origin feature/<ten-tinh-nang>
   ```
4. **Tạo Pull Request (PR) trên GitHub** để nhóm trưởng duyệt và gộp vào nhánh chính `main`.

---
© 2026 UteTechStore • Nền tảng thương mại điện tử công nghệ cao cấp.
