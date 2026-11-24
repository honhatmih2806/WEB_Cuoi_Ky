#!/usr/bin/env bash
set -e

echo "🚀 [TECH STORE Local Dev] Khởi chạy Backend & Database..."

if [ ! -f .env ]; then
  cp .env.example .env 2>/dev/null || true
fi

export DISABLE_SQLALCHEMY_CEXT=1

# Kích hoạt venv (hỗ trợ cả Windows Git Bash và Linux/macOS)
if [ -f ".venv/Scripts/activate" ]; then
  source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi

PYTHON_BIN="python"
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
fi

echo "🌱 Kiểm tra và nạp dữ liệu danh mục & sản phẩm..."
PYTHONPATH=apps/api $PYTHON_BIN scripts/init_db.py 2>/dev/null || true
PYTHONPATH=apps/api $PYTHON_BIN scripts/seed_products.py 2>/dev/null || true

echo ""
echo "=========================================================================="
echo "✅ Hệ thống Tech Store Backend đã sẵn sàng!"
echo "👉 Swagger API: http://localhost:8000/docs"
echo "👉 Để chạy Frontend Web Next.js trong terminal khác:"
echo "   cd apps/web && npm run dev"
echo "=========================================================================="
echo ""

cd apps/api
$PYTHON_BIN -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
