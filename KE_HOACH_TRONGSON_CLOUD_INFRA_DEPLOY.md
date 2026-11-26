# 🌐 KẾ HOẠCH CÔNG VIỆC — TRỌNG SƠN (CLOUD TEAM 2)

> **Dự án:** UteTechStore — Cloud-Native E-Commerce & Media Processing  
> **Thành viên:** **TrongSon**  
> **Vai trò:** Cloud Infrastructure, Database RDS, Docker & Monitoring Engineer (VPC, IAM, RDS, Docker/LocalStack, ALB, CloudWatch)  
> **Nhánh Git làm việc:** `feature/cloud-infra-deploy`  

---

## 🎯 1. Ý Tưởng & Mục Tiêu

Bạn chịu trách nhiệm **đưa toàn bộ hạ tầng web `UteTechStore` lên chuẩn Cloud** (bao phủ Module 3, 4, 5, 8, 9, 10 của AWS):
1. Chuẩn hóa `docker-compose.yml` và tích hợp **LocalStack** để cả nhóm có thể chạy thử S3 + Lambda + CloudWatch ngay trên máy cá nhân mà không tốn chi phí.
2. Cấu hình kết nối **Amazon RDS (PostgreSQL)** thay cho SQLite cục bộ.
3. Thiết kế kiến trúc mạng **VPC (Public/Private Subnet)**, phân quyền bảo mật **IAM Role + Security Group**, cân bằng tải **ALB + Auto Scaling**, và **CloudWatch Logging/Alerting**.

---

## 🛠️ 2. Các File Bạn Cần Tạo Mới & Chỉnh Sửa

| Thao tác | Đường dẫn File | Nội dung thực hiện |
| :---: | :--- | :--- |
| **Chỉnh sửa** | `docker-compose.yml` | Đổi tên container `titan-silicon-*` sang `utetechstore-*`, thêm service `localstack` (mở port `4566`, bật dịch vụ `s3,lambda,logs`) và truyền biến `AWS_ENDPOINT_URL=http://localstack:4566` cho service `api`. |
| **Tạo mới** | `cloud/localstack/init-aws.sh` | Script tự khởi tạo khi LocalStack chạy: tạo bucket `utetechstore-assets`, đóng gói & deploy Lambda của **NgocHuy**, gắn S3 Event Notification cho prefix `raw/`. |
| **Chỉnh sửa** | `.env.example` | Cập nhật template biến môi trường chuẩn cho cả 2 chế độ: Local Docker/LocalStack và AWS Production (RDS `DATABASE_URL`, S3 Bucket, CloudFront). |
| **Chỉnh sửa** | `apps/api/main.py` | Bổ sung cấu hình **Structured JSON Logging** (tương thích AWS CloudWatch Logs) và cập nhật `/health` kiểm tra trạng thái kết nối Database + S3. |
| **Tạo mới** | `docs/CLOUD_ARCHITECTURE_AWS.md` | Tài liệu đặc tả hạ tầng AWS (VPC CIDR, Public/Private Subnet, IAM Least Privilege Policy, Security Group rules, ALB + ASG, CloudWatch Alarm + SNS, bảng dự toán chi phí AWS Pricing Calculator). |

---

## 🚀 3. Hướng Dẫn Triển Khai Chi Tiết

### Bước 1: Mở nhánh Git riêng
```bash
git checkout main
git pull origin main
git checkout -b feature/cloud-infra-deploy
```

### Bước 2: Cập nhật `docker-compose.yml` & tạo `cloud/localstack/init-aws.sh`
- Trong `docker-compose.yml`:
  - Đổi `container_name` từ `titan-silicon-postgres`, `titan-silicon-redis`, `titan-silicon-api`, `titan-silicon-web` thành `utetechstore-postgres`, `utetechstore-redis`, `utetechstore-api`, `utetechstore-web`.
  - Thêm service `localstack`:
    ```yaml
    localstack:
      image: localstack/localstack:latest
      container_name: utetechstore-localstack
      ports:
        - "4566:4566"
      environment:
        - SERVICES=s3,lambda,logs
        - DEFAULT_REGION=ap-southeast-1
      volumes:
        - ./cloud/localstack/init-aws.sh:/etc/localstack/init/ready.d/init-aws.sh
        - ./cloud/lambda_watermark:/opt/lambda_watermark
    ```
  - Thêm `AWS_ENDPOINT_URL=http://localstack:4566` vào `environment` của service `api`.

### Bước 3: Chuyển đổi Database sang PostgreSQL / Amazon RDS
- Code trong `apps/api/core/config.py` đã đọc `DATABASE_URL` từ biến môi trường.
- Cập nhật `.env.example` với mẫu kết nối RDS:
  `DATABASE_URL=postgresql+psycopg://<username>:<password>@<rds-endpoint>:5432/utetechstore_db`
- Viết hướng dẫn tạo RDS PostgreSQL (Private Subnet, tắt Public Access, chỉ mở port `5432` cho Security Group của EC2/API) vào `docs/CLOUD_ARCHITECTURE_AWS.md`.

### Bước 4: Chuẩn hóa Logging cho CloudWatch tại `apps/api/main.py`
- Cấu hình Python `logging` xuất log định dạng rõ ràng (`timestamp`, `level`, `method`, `path`, `process_time`) để khi chạy trên EC2 / ECS, CloudWatch Logs Agent thu thập và lọc lỗi `5xx` dễ dàng.

---

## 🤝 4. Điểm Phối Hợp Với Các Thành Viên Khác

- **Với NgocHuy (Cloud 1):** Nhận đường dẫn `cloud/lambda_watermark/handler.py` để gắn vào `cloud/localstack/init-aws.sh` và kiểm tra trigger tự động khi upload file vào bucket `utetechstore-assets`.
- **Với DangKhoa & HuynhHuong (Web Team):** Khi 2 bạn Web cần test full-stack với S3 giả lập và PostgreSQL, chỉ cần chạy `docker compose up --build`.

---

## ✅ 5. Tiêu Chí Nghiệm Thu (Definition of Done)

- [ ] `docker compose up -d` khởi chạy thành công cả 5 container (`postgres`, `redis`, `localstack`, `api`, `web`).
- [ ] LocalStack tự tạo sẵn bucket `utetechstore-assets` ngay khi khởi động.
- [ ] Endpoint `GET /health` trả về trạng thái `HEALTHY` cùng thông tin Database (`postgresql` / `sqlite`).
- [ ] File `docs/CLOUD_ARCHITECTURE_AWS.md` hoàn chỉnh đầy đủ thiết kế VPC, IAM, Security Group, RDS, ALB, Auto Scaling, CloudWatch và dự toán chi phí.
- [ ] Push code lên nhánh `feature/cloud-infra-deploy` và tạo Pull Request vào `main`.
