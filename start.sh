#!/usr/bin/env bash
set -e

echo "🚀 [TECH STORE JAPAN] Đang khởi động toàn bộ hệ thống..."

if [ ! -f .env ]; then
  echo "⚠️ Không tìm thấy file .env, tự động tạo từ .env.example..."
  cp .env.example .env 2>/dev/null || true
fi

export DISABLE_SQLALCHEMY_CEXT=1

# Check if docker is installed and running
HAS_DOCKER=false
if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    HAS_DOCKER=true
  fi
fi

if [ "$HAS_DOCKER" = true ]; then
  if docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
  else
    DOCKER_COMPOSE="docker-compose"
  fi
  echo "📦 Khởi chạy với $DOCKER_COMPOSE..."
  $DOCKER_COMPOSE up -d --build
  echo "⏳ Đang kiểm tra kết nối CSDL và nạp dữ liệu danh mục & sản phẩm..."
  sleep 4
  $DOCKER_COMPOSE exec -T api python /scripts/init_db.py || true
  $DOCKER_COMPOSE exec -T api python /scripts/seed_products.py || true
else
  echo "ℹ️ Môi trường không có Docker daemon, tự động chuyển sang chế độ Local Native..."
  
  # Activate venv if present
  if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
  elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
  fi

  PYTHON_BIN="python"
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  fi

  echo "🌱 Đang nạp dữ liệu SQLite nếu chưa có..."
  PYTHONPATH=apps/api $PYTHON_BIN scripts/init_db.py 2>/dev/null || true
  PYTHONPATH=apps/api $PYTHON_BIN scripts/seed_products.py 2>/dev/null || true

  echo "⚡ Khởi chạy Backend FastAPI..."
  (cd apps/api && $PYTHON_BIN -m uvicorn main:app --host 127.0.0.1 --port 8000 &)

  echo "⚡ Khởi chạy Frontend Next.js..."
  (cd apps/web && npm run dev &)
fi

echo ""
echo "=========================================================================="
echo "✅ CỬA HÀNG TECH STORE JAPAN ĐÃ SẴN SÀNG!"



echo "👉 Cửa hàng Web (Next.js 14):  http://localhost:3000"
echo "👉 Tài liệu Swagger API (FastAPI): http://localhost:8000/docs"
echo "👉 Kiểm tra sức khỏe hệ thống:     http://localhost:8000/health"
echo "=========================================================================="
echo ""
