# DEPLOYMENT.md — Titan Silicon Production Deployment Guide

Tài liệu này cung cấp hướng dẫn chi tiết toàn diện từ A-Z để đóng gói, thiết lập hạ tầng và triển khai (Deploy) hệ thống **Titan Silicon: Apple & NVIDIA Flagship Platform** lên các môi trường thực tế:
1. **Triển khai tự động bằng Docker & Docker Compose (Production Stack)**
2. **Triển khai trên Cloud VPS (Ubuntu 22.04 / 24.04 LTS) với Nginx Reverse Proxy & SSL Let's Encrypt**
3. **Triển khai theo mô hình Hybrid Cloud (Frontend Next.js trên Vercel + Backend FastAPI trên Railway / Render)**
4. **Quy trình Tự động hóa CI/CD với GitHub Actions**
5. **Giám sát (Monitoring) & Sao lưu (Backup) cơ sở dữ liệu**

---

## 1. Kiến Trúc Hạ Tầng Triển Khai (Infrastructure Topology)

```
                            [ Khách hàng / Trình duyệt ]
                                         │
                                         ▼ HTTPS:443
                        [ Cloudflare DNS & DDoS Protection ]
                                         │
                                         ▼
                 [ VPS Nginx Reverse Proxy (SSL Certbot Let's Encrypt) ]
                        │                                    │
           Proxy :3000  │                                    │ Proxy :8000
                        ▼                                    ▼
       [ Docker: titan-web (Next.js 14) ]    [ Docker: titan-api (FastAPI) ]
                                                             │
                                              Internal Net   │
                                                             ▼
                                             [ Docker: PostgreSQL 16 + Redis ]
```

---

## 2. Triển Khai Phương Án 1: Docker Compose Trên Cloud VPS

### 2.1. Yêu cầu phần cứng khuyến nghị (Server Specs)
* **CPU:** 2 vCPU trở lên
* **RAM:** 4GB trở lên (khuyến nghị 8GB nếu chạy chung PostgreSQL và Redis)
* **Ổ cứng:** 40GB SSD / NVMe
* **HĐH:** Ubuntu 22.04 LTS hoặc 24.04 LTS 64-bit

### 2.2. Chuẩn bị VPS
```bash
# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài đặt Docker & Docker Compose Plugin
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Cấp quyền cho user hiện tại chạy docker không cần sudo
sudo usermod -aG docker $USER
newgrp docker
```

### 2.3. Cấu hình biến môi trường Production
Tạo file `.env.production` tại thư mục dự án:
```ini
# Production Environment
ENVIRONMENT=production
PROJECT_NAME="Titan Silicon Flagship Platform"
VERSION=1.0.0

# Database Credentials
POSTGRES_USER=titan_prod_admin
POSTGRES_PASSWORD=YourUltraSecurePassword_2026!
POSTGRES_DB=titan_silicon_db
DATABASE_URL=postgresql://titan_prod_admin:YourUltraSecurePassword_2026!@postgres:5432/titan_silicon_db

# Cache & Message Broker
REDIS_URL=redis://redis:6379/0

# Security Keys
JWT_SECRET=f39a8c7b8d0e123456789abcdef0123456789abcdef0123456789abcdef01234
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# Public Domain
NEXT_PUBLIC_API_URL=https://api.titansilicon.vn/api/v1
```

### 2.4. Khởi chạy toàn bộ hệ thống
```bash
# Build và chạy ngầm toàn bộ dịch vụ
docker compose -f docker-compose.yml --env-file .env.production up -d --build

# Kiểm tra trạng thái containers
docker compose ps

# Nạp dữ liệu danh mục & sản phẩm mẫu iPhone & NVIDIA
docker compose exec api python scripts/init_db.py
docker compose exec api python scripts/seed_products.py
```

---

## 3. Cấu Hình Nginx Reverse Proxy & Chứng Chỉ SSL HTTPS

### 3.1. Cài đặt Nginx & Certbot
```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

### 3.2. Cấu hình Server Block cho Domain
Tạo file `/etc/nginx/sites-available/titansilicon.conf`:
```nginx
# 1. Cấu hình Frontend (Web App)
server {
    server_name titansilicon.vn www.titansilicon.vn;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 2. Cấu hình Backend API
server {
    server_name api.titansilicon.vn;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
    }
}
```

Kích hoạt và cấp chứng chỉ SSL miễn phí tự gia hạn:
```bash
sudo ln -s /etc/nginx/sites-available/titansilicon.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Tự động cấu hình SSL Let's Encrypt
sudo certbot --nginx -d titansilicon.vn -d www.titansilicon.vn -d api.titansilicon.vn
```

---

## 4. Triển Khai Phương Án 2: Serverless / Hybrid Cloud (Vercel + Railway)

Dành cho kịch bản triển khai siêu nhanh, không cần quản trị máy chủ Linux:
1. **Frontend (Next.js 14):**
   * Đẩy mã nguồn lên GitHub.
   * Truy cập [Vercel](https://vercel.com) -> New Project -> Chọn thư mục `apps/web`.
   * Thêm Environment Variable: `NEXT_PUBLIC_API_URL=https://your-api.up.railway.app/api/v1`.
   * Bấm **Deploy**.
2. **Backend (FastAPI & PostgreSQL):**
   * Tạo project mới trên [Railway](https://railway.app) hoặc [Render](https://render.com).
   * Tạo 1 Database PostgreSQL (tích hợp sẵn pgvector).
   * Triển khai dịch vụ từ thư mục `apps/api`.
   * Cung cấp biến môi trường `DATABASE_URL` lấy từ kết nối PostgreSQL của Railway.

---

## 5. Quy Trình CI/CD Tự Động Hóa (GitHub Actions)

Tạo file `.github/workflows/deploy.yml`:
```yaml
name: Deploy Titan Silicon Production

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Execute Remote SSH Commands
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd /opt/titan-silicon
            git pull origin main
            docker compose down
            docker compose up -d --build
            docker compose exec -T api python scripts/init_db.py
            docker compose exec -T api python scripts/seed_products.py
```

---

## 6. Chiến Lược Sao Lưu & Phục Hồi Dữ Liệu (Backup & Disaster Recovery)

Thiết lập cronjob sao lưu cơ sở dữ liệu hàng đêm lúc 2:00 sáng:
```bash
# Mở crontab
crontab -e

# Thêm dòng sau:
0 2 * * * docker compose -f /opt/titan-silicon/docker-compose.yml exec -T postgres pg_dump -U titan_prod_admin titan_silicon_db | gzip > /opt/backups/titan_db_$(date +\%Y\%m\%d_\%H\%M\%S).sql.gz
```
Lệnh khôi phục khi gặp sự cố:
```bash
gunzip < /opt/backups/titan_db_20261123_020000.sql.gz | docker compose exec -T postgres psql -U titan_prod_admin -d titan_silicon_db
```
