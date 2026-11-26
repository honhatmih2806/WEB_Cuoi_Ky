# UteTechStore — Nền Tảng Thương Mại Điện Tử & Xử Lý Media Trên Đám Mây (Web + AWS Cloud)

[![Next.js 14](https://img.shields.io/badge/Next.js-14%20App%20Router-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.165+-green.svg)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4+-38bdf8.svg)](https://tailwindcss.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4+-blue.svg)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-yellow.svg)](https://python.org/)
[![AWS Cloud](https://img.shields.io/badge/AWS-S3%20%7C%20SQS%20%7C%20Lambda%20%7C%20RDS-orange.svg)](./docs/CLOUD_ARCHITECTURE_AWS.md)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-indigo.svg)](https://www.postgresql.org/)

> **UteTechStore** là nền tảng thương mại điện tử thiết bị công nghệ cao cấp kết hợp kiến trúc **Cloud-Native trên AWS** (tự động tạo Thumbnail 16:9 và đóng dấu Watermark cho ảnh sản phẩm & Catalogue/Datasheet PDF). Dự án được xây dựng với giao diện tối giản, tươi sáng, tích hợp đầy đủ quy trình mua sắm, định giá thu cũ đổi mới và triển khai hạ tầng đám mây chuẩn **Well-Architected Framework**.

---

## 🌐 Đường Dẫn Truy Cập Nhanh

* **Cửa Hàng Trực Tuyến (Next.js 14):** [http://localhost:3000](http://localhost:3000)
* **Tài Liệu Backend API (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Kiểm Tra Sức Khỏe Hệ Thống:** [http://localhost:8000/health](http://localhost:8000/health)
* **Tài Liệu Kiến Trúc Đám Mây AWS:** [docs/CLOUD_ARCHITECTURE_AWS.md](./docs/CLOUD_ARCHITECTURE_AWS.md)

---

## ☁️ Kiến Trúc Hệ Thống & Tích Hợp Cloud

Hệ thống kết hợp giữa **Web Application (Next.js 14 + FastAPI)** và **Hạ tầng Đám mây AWS** (bao phủ đầy đủ 10 Modules AWS Cloud Foundations):

* **Networking & Bảo mật biên:** `Route 53` $\rightarrow$ `CloudFront (HTTPS/ACM + AWS WAF)` $\rightarrow$ `Application Load Balancer (ALB)` phân tải trên 2 Availability Zones (`ap-southeast-1a`, `1b`).
* **VPC & Security:** VPC `10.0.0.0/16` tách biệt Public Subnet (ALB, NAT Gateway) và Private Subnet (App EC2/ECS, RDS PostgreSQL, Redis), áp dụng **IAM Least Privilege**, **Security Groups 3 lớp** và **AWS Secrets Manager**.
* **Xử lý Media Bất đồng bộ (Event-Driven):** Upload ảnh sản phẩm / PDF Catalogue lên **Amazon S3 (`raw/`)** qua Presigned URL $\rightarrow$ **Amazon SQS (kèm DLQ)** $\rightarrow$ **AWS Lambda** *(hoặc ECS Fargate Worker cho file > 200 trang)* tự động sinh Thumbnail (`320×180`, `640×360`, `1280×720`) và đóng Watermark `UteTechStore` vào `processed/`.
* **Database & Giám sát:** **SQLite (`titan_silicon.db`)** ở Local Dev và **Amazon RDS PostgreSQL 16 (Multi-AZ)** trên Cloud, tích hợp **ElastiCache Redis**, **CloudWatch Logs/Alarms + SNS** và **LocalStack** để chạy mô phỏng AWS ngay trên máy cá nhân.

👉 Xem chi tiết thiết kế mạng, IAM, S3 Lifecycle, Idempotency, RTO/RPO, CI/CD và dự toán chi phí tại: **[docs/CLOUD_ARCHITECTURE_AWS.md](./docs/CLOUD_ARCHITECTURE_AWS.md)**

---

## 👥 Phân Công Nhiệm Vụ Nhóm (4 Thành Viên)

Mỗi thành viên làm việc trên một nhánh riêng (`feature/...`) và sở hữu nhóm file độc lập để tránh xung đột code:

| Thành Viên | Nhóm | Nhánh Git | Trách Nhiệm Chính | Kế Hoạch Chi Tiết |
| :--- | :---: | :--- | :--- | :--- |
| **Ngọc Huy** | Cloud 1 | `feature/cloud-s3-lambda` | Amazon S3 (`raw/`, `processed/`), AWS Lambda Thumbnail/Watermark & `s3_service.py` | [KE_HOACH_NGOCHUY_CLOUD_STORAGE_LAMBDA.md](./KE_HOACH_NGOCHUY_CLOUD_STORAGE_LAMBDA.md) |
| **Trọng Sơn** | Cloud 2 | `feature/cloud-infra-deploy` | Docker + LocalStack, RDS PostgreSQL, VPC/IAM/Security Groups, CloudWatch & CI/CD | [KE_HOACH_TRONGSON_CLOUD_INFRA_DEPLOY.md](./KE_HOACH_TRONGSON_CLOUD_INFRA_DEPLOY.md) |
| **Huỳnh Hương** | Web 1 | `feature/web-ui-data-media` | Tinh giản Data sản phẩm, Bộ lọc khoảng giá, Modal Định giá Thu cũ & Trang `/documents` | [KE_HOACH_HUYNHHUONG_WEB_DATA_MEDIA_UI.md](./KE_HOACH_HUYNHHUONG_WEB_DATA_MEDIA_UI.md) |
| **Đăng Khoa** | Web 2 | `feature/web-backend-search-pricing` | Backend Tìm kiếm đa từ khóa/giá, API Định giá Trade-in & API Cloud Documents Bridge | [KE_HOACH_DANGKHOA_WEB_BACKEND_API_SEARCH.md](./KE_HOACH_DANGKHOA_WEB_BACKEND_API_SEARCH.md) |

---

## ⚡ Hướng Dẫn Khởi Chạy Nhanh (Quick Start)

| Môi Trường / Terminal | Lệnh Thực Thi | Mô Tả |
| :--- | :--- | :--- |
| **Windows PowerShell** | `.\start.ps1` | Script chuyên dụng cho PowerShell, tự kích hoạt `.venv` & mở trình duyệt |
| **Windows (1-Click UI)** | Nhấp đúp **`start.bat`** *(hoặc `run_store.bat`)* | Tự động khởi chạy đồng thời Backend (`:8000`) & Frontend (`:3000`) |
| **Mọi hệ điều hành (Python)** | `python scripts/start_servers.py` | Chạy đồng thời cả 2 server trên cùng 1 terminal |
| **Git Bash / Linux / macOS** | `./start.sh` *(hoặc `bash start.sh`)* | Tự nhận diện Docker Compose hoặc chế độ Local Native |

> [!NOTE]
> Trên **Windows PowerShell (`PS C:\...`)**, hãy dùng **`.\start.ps1`** hoặc **`.\start.bat`**. Không gõ `./start.sh` trong PowerShell vì PowerShell không thực thi trực tiếp shell script của Linux.

---

## 🛠️ Cài Đặt Thủ Công Cho Thành Viên Mới

### 1. Clone Kho Mã Nguồn
```bash
git clone https://github.com/honhatmih2806/WEB_Cuoi_Ky.git
cd WEB_Cuoi_Ky
```

### 2. Khởi chạy Backend (FastAPI)
```powershell
python -m venv .venv
.\.venv\Scripts\activate        # Windows (Mac/Linux: source .venv/bin/activate)
pip install -r apps/api/requirements.txt
cd apps/api
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Khởi chạy Frontend (Next.js 14)
```powershell
cd apps/web
npm install
npm run dev
```

---

## 📁 Cấu Trúc Thư Mục Dự Án

```text
.
├── apps/
│   ├── api/                                      # Backend FastAPI (Python 3.12)
│   │   ├── core/                                 # Config, Database, Envelope, Exceptions
│   │   ├── models/                               # SQLAlchemy Entities
│   │   ├── routers/                              # API Controllers (products, categories, orders, advisor...)
│   │   └── main.py                               # FastAPI entry point
│   └── web/                                      # Frontend Next.js 14 (App Router, Tailwind CSS)
│       └── src/
│           ├── app/                              # App Router (globals.css, layout.tsx, page.tsx)
│           ├── components/                       # Navbar, HeroBanner, ProductCard, Cart, Checkout...
│           ├── services/                         # API Client & Fallback Data
│           └── types/                            # TypeScript DTOs
├── docs/
│   └── CLOUD_ARCHITECTURE_AWS.md                 # Tài liệu Kiến trúc AWS Cloud toàn diện
├── scripts/
│   ├── seed_products.py                          # Nạp dữ liệu sản phẩm vào SQLite/PostgreSQL
│   └── start_servers.py                          # Chạy đồng thời Backend & Frontend
├── KE_HOACH_NGOCHUY_CLOUD_STORAGE_LAMBDA.md      # Kế hoạch Thành viên Cloud 1
├── KE_HOACH_TRONGSON_CLOUD_INFRA_DEPLOY.md       # Kế hoạch Thành viên Cloud 2
├── KE_HOACH_HUYNHHUONG_WEB_DATA_MEDIA_UI.md      # Kế hoạch Thành viên Web 1
├── KE_HOACH_DANGKHOA_WEB_BACKEND_API_SEARCH.md   # Kế hoạch Thành viên Web 2
├── docker-compose.yml                            # Môi trường Container (Postgres, Redis, API, Web)
├── start.ps1 / start.bat / start.sh              # Các kịch bản khởi chạy nhanh
└── README.md
```

---

## 🔀 Quy Trình Làm Việc Trên Git

1. Tạo nhánh riêng theo đúng tên nhánh trong bảng phân công:
   ```bash
   git checkout -b feature/<ten-nhanh-cua-ban>
   ```
2. Code, kiểm thử chạy ổn định trên máy cá nhân, sau đó commit & push:
   ```bash
   git add .
   git commit -m "feat: mo ta ngan gon cong viec"
   git push origin feature/<ten-nhanh-cua-ban>
   ```
3. Tạo **Pull Request (PR)** trên GitHub để nhóm trưởng review và merge vào `main`.

---
© 2026 **UteTechStore** • Cloud-Native E-Commerce & Automated Media Processing Platform.
