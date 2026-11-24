# SETUP.md — Hướng Dẫn Cài Đặt & Chạy Cửa Hàng Titan Silicon

---

## 1. Yêu Cầu Môi Trường (Prerequisites)

* **Hệ điều hành:** Linux, macOS, hoặc Windows WSL2.
* **Python:** ≥ 3.10 (khuyến nghị Python 3.11 - 3.14).
* **Node.js:** ≥ 18.x (khuyến nghị Node 20.x hoặc 22.x).
* **Docker & Docker Compose:** Đã cài đặt (khuyến nghị cho môi trường đồng bộ).

---

## 2. Khởi Động Siêu Nhanh 1 Lệnh (Quick Start)

Chỉ cần chạy lệnh sau tại thư mục gốc:

```bash
./start.sh
```

Hoặc dùng `Makefile`:
```bash
make up
```

Hệ thống sẽ tự động:
1. Khởi động PostgreSQL và Redis
2. Tự động khởi tạo Database và seed 18+ sản phẩm iPhone, NVIDIA, Combo Studio
3. Chạy Backend API tại: `http://localhost:8000` (Swagger UI: `http://localhost:8000/docs`)
4. Chạy Web Frontend tại: `http://localhost:3000`

---

## 3. Chạy Môi Trường Phát Triển Từng Phần (Local Dev)

### 3.1. Thiết lập Backend API
```bash
cd apps/api
# Tạo môi trường ảo nếu chưa có
python3 -m venv .venv
source .venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt

# Khởi tạo CSDL và nạp dữ liệu mẫu
python ../../scripts/init_db.py
python ../../scripts/seed_products.py

# Khởi chạy server API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3.2. Thiết lập Web Frontend
```bash
cd apps/web
npm install
npm run dev
```

Truy cập trình duyệt: `http://localhost:3000`.
