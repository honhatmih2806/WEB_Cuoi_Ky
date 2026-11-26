# UteTechStore — Nền Tảng Thương Mại Điện Tử & Hạ Tầng Cloud-Native (AWS)

[![Next.js 14](https://img.shields.io/badge/Next.js-14%20App%20Router-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.165+-green.svg)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4+-38bdf8.svg)](https://tailwindcss.com/)
[![PostgreSQL / SQLite](https://img.shields.io/badge/Database-RDS%20PostgreSQL%20%7C%20SQLite-indigo.svg)](https://www.postgresql.org/)
[![AWS Cloud](https://img.shields.io/badge/Cloud-AWS%20S3%20%7C%20SQS%20%7C%20Lambda%20%7C%20LocalStack-orange.svg)](https://aws.amazon.com/)
[![Status](https://img.shields.io/badge/Status-Active%20Development-emerald.svg)]()

> **UteTechStore** là nền tảng thương mại điện tử chuyên phân phối các thiết bị điện tử & công nghệ cao cấp, được thiết kế theo **kiến trúc Cloud-Native trên AWS** kết hợp hệ thống xử lý ảnh sản phẩm và PDF Catalogue/Datasheet tự động (**Thumbnail & Watermark Event-Driven**).

---

## 🌐 Đường Dẫn Truy Cập Local

* **Cửa Hàng Trực Tuyến (Next.js 14):** [http://localhost:3000](http://localhost:3000)
* **Tài Liệu Backend API (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Kiểm Tra Trạng Thái Hệ Thống:** [http://localhost:8000/health](http://localhost:8000/health)

---

## ⚡ Hướng Dẫn Khởi Chạy Nhanh (Quick Start)

| Môi Trường / Terminal | Lệnh Thực Thi | Mô Tả |
| :--- | :--- | :--- |
| **Windows PowerShell** | `.\start.ps1` | Script chuyên dụng cho PowerShell, tự cấu hình môi trường |
| **Windows (1-Click UI)** | Nhấp đúp **`start.bat`** *(hoặc `run_store.bat`)* | Tự bật Backend (`:8000`) & Frontend (`:3000`), tự mở trình duyệt |
| **Mọi hệ điều hành (Python)** | `python scripts/start_servers.py` | Chạy đồng thời cả 2 server trên cùng 1 terminal |
| **Git Bash / Linux / macOS** | `./start.sh` *(hoặc `bash start.sh`)* | Tự nhận diện môi trường Docker / Local Native |

> [!NOTE]
> Nếu dùng **Windows PowerShell** (`PS C:\...`), hãy chạy **`.\start.ps1`** hoặc **`.\start.bat`** (không gõ `./start.sh` vì PowerShell không tự thực thi shell script của Linux).

---

## ☁️ Kiến Trúc Cloud & Tính Năng Nổi Bật

### 1. Kiến Trúc Đám Mây AWS Toàn Diện ([Chi tiết tại đây](./docs/CLOUD_ARCHITECTURE_AWS.md))
* **Network & Delivery:** VPC `10.0.0.0/16` (Public/Private App/Private DB Subnets trên 2 AZs `ap-southeast-1`), Route 53 + ACM (TLS 1.3) + **CloudFront CDN** + **AWS WAF** + Application Load Balancer (ALB).
* **Serverless Media Pipeline:** `Amazon S3 (raw/)` $\rightarrow$ `S3 Event Notification` $\rightarrow$ `Amazon SQS + DLQ` $\rightarrow$ `AWS Lambda` *(hoặc `ECS Fargate` cho PDF > 200 trang)* tự động sinh Thumbnail 16:9 (`320×180`, `640×360`, `1280×720`) và đóng Watermark `UteTechStore` vào `processed/`.
* **Database, Security & Monitoring:** **Amazon RDS PostgreSQL 16 (Multi-AZ)** + **ElastiCache Redis**, **IAM Least Privilege**, **Secrets Manager**, **CloudWatch Logs/Alarms + SNS**.

### 2. Nền Tảng Web Thương Mại Điện Tử (`Next.js 14` + `FastAPI`)
* **Giao diện tối giản sáng (Luxury Minimalist):** Tông trắng tinh khiết (`#FFFFFF` / `#F8F9FA`), đường viền mảnh (`#E5E7EB`), typography rõ ràng không lạm dụng icon trang trí.
* **Tính năng mua sắm đầy đủ:** Tìm kiếm đa từ khóa, lọc theo hãng/danh mục/khoảng giá, công cụ định giá Thu cũ Đổi mới (Trade-in), giỏ hàng thời gian thực (mã `UTEVIP`, `LUXURY`, `UTETECHSTORE`), thanh toán **VietQR**, tra cứu đơn hàng (`ORD-2026-XXXXX`), và cơ chế **Fallback Zero-Downtime**.

---

## 👥 Phân Công Nhiệm Vụ Đội Ngũ (4 Thành Viên)

| Thành Viên | Nhóm | Nhánh Git | Trách Nhiệm Chính | Kế Hoạch Chi Tiết |
| :--- | :---: | :--- | :--- | :--- |
| **Ngọc Huy** | Cloud 1 | `feature/cloud-s3-lambda` | Amazon S3 (`raw/` & `processed/`), `boto3` Service, AWS Lambda Thumbnail & Watermark | [KE_HOACH_NGOCHUY_CLOUD_STORAGE_LAMBDA.md](./KE_HOACH_NGOCHUY_CLOUD_STORAGE_LAMBDA.md) |
| **Trọng Sơn** | Cloud 2 | `feature/cloud-infra-deploy` | Docker + LocalStack, RDS PostgreSQL, VPC/IAM/SG, ALB/ASG, CloudWatch Logs | [KE_HOACH_TRONGSON_CLOUD_INFRA_DEPLOY.md](./KE_HOACH_TRONGSON_CLOUD_INFRA_DEPLOY.md) |
| **Huỳnh Hương** | Web 1 | `feature/web-ui-data-media` | Tinh giản Data sản phẩm, UI Lọc giá, Trade-in Modal & Trang Cloud Gallery `/documents` | [KE_HOACH_HUYNHHUONG_WEB_DATA_MEDIA_UI.md](./KE_HOACH_HUYNHHUONG_WEB_DATA_MEDIA_UI.md) |
| **Đăng Khoa** | Web 2 | `feature/web-backend-search-pricing` | Backend Search/Lọc giá, API Định giá `pricing.py`, Router `documents.py` & `api.ts` | [KE_HOACH_DANGKHOA_WEB_BACKEND_API_SEARCH.md](./KE_HOACH_DANGKHOA_WEB_BACKEND_API_SEARCH.md) |

---

## 📁 Cấu Trúc Mã Nguồn

```text
.
├── apps/
│   ├── api/                  # FastAPI Backend (Python 3.12)
│   │   ├── core/             # Config, Database, ApiResponse Envelope, Exceptions
│   │   ├── models/           # SQLAlchemy Entities (Product, Category, Order, SlideDocument...)
│   │   ├── routers/          # API Controllers (products, categories, orders, advisor, pricing, documents)
│   │   ├── services/         # S3 Service (boto3) & Processing Helpers
│   │   └── main.py           # FastAPI entry point
│   └── web/                  # Next.js 14 Frontend (App Router, TypeScript, Tailwind CSS)
│       └── src/
│           ├── app/          # App Router (page.tsx, documents/page.tsx, layout.tsx)
│           ├── components/   # Navbar, HeroBanner, ProductCard, TradeInModal, CartDrawer, CheckoutModal...
│           └── services/     # API Client & Fallback Data
├── docs/
│   └── CLOUD_ARCHITECTURE_AWS.md   # Tài liệu Kiến trúc AWS Cloud toàn diện (Modules 1-10)
├── scripts/
│   ├── seed_products.py      # Script nạp dữ liệu sản phẩm vào SQLite/PostgreSQL
│   └── start_servers.py      # Script chạy nền đồng thời cả Backend và Frontend
├── start.ps1 / start.bat     # Kịch bản khởi chạy 1-click trên Windows
├── start.sh / dev.sh         # Kịch bản khởi chạy trên Linux / macOS / Git Bash
├── docker-compose.yml        # Docker Stack (PostgreSQL, Redis, LocalStack, API, Web)
└── KE_HOACH_*.md             # 4 tệp kế hoạch chi tiết cho từng thành viên
```

---

## 🔀 Quy Trình Làm Việc Trên Git (Team Workflow)

1. **Clone kho mã nguồn:**
   ```bash
   git clone https://github.com/honhatmih2806/WEB_Cuoi_Ky.git
   cd WEB_Cuoi_Ky
   ```
2. **Tạo đúng nhánh riêng được phân công (không commit trực tiếp lên `main`):**
   ```bash
   git checkout -b <ten-nhanh-cua-ban>
   ```
3. **Code, kiểm thử tại local, sau đó commit và push nhánh lên GitHub:**
   ```bash
   git add .
   git commit -m "feat: mô tả công việc đã hoàn thành"
   git push origin <ten-nhanh-cua-ban>
   ```
4. **Tạo Pull Request (PR)** trên GitHub để Trưởng nhóm review và merge vào `main`.

---
© 2026 UteTechStore • Cloud-Native Electronics E-Commerce & Media Processing Platform.
