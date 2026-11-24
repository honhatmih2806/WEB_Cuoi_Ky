DOCKER_COMPOSE ?= $(shell docker compose version >/dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

.PHONY: help up down restart logs build init-db seed test clean dev-api dev-web

help:
	@echo "======================================================================"
	@echo "  TITAN SILICON — Apple & NVIDIA Ecosystem Flagship Platform"
	@echo "======================================================================"
	@echo "  make up        - Khởi chạy toàn bộ hệ thống bằng Docker Compose"
	@echo "  make down      - Dừng toàn bộ các container"
	@echo "  make restart   - Khởi động lại hệ thống"
	@echo "  make logs      - Xem logs realtime của API và Web"
	@echo "  make init-db   - Khởi tạo Database schema"
	@echo "  make seed      - Nạp dữ liệu sản phẩm mẫu iPhone & NVIDIA & Bundles"
	@echo "  make dev-api   - Khởi chạy Backend FastAPI ở chế độ dev reload"
	@echo "  make dev-web   - Khởi chạy Frontend Next.js ở chế độ dev"
	@echo "  make clean     - Dọn dẹp cache tạm"

up:
	$(DOCKER_COMPOSE) up -d --build
	@echo "⏳ Đang đợi cơ sở dữ liệu khởi động..."
	@sleep 3
	$(DOCKER_COMPOSE) exec api python /scripts/init_db.py
	$(DOCKER_COMPOSE) exec api python /scripts/seed_products.py
	@echo "✅ Hệ thống Titan Silicon đã khởi chạy thành công!"
	@echo "👉 Frontend Web: http://localhost:3000"
	@echo "👉 Swagger API:  http://localhost:8000/docs"

down:
	$(DOCKER_COMPOSE) down

restart: down up

logs:
	$(DOCKER_COMPOSE) logs -f api web

init-db:
	$(DOCKER_COMPOSE) exec api python /scripts/init_db.py

seed:
	$(DOCKER_COMPOSE) exec api python /scripts/seed_products.py

dev-api:
	cd apps/api && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-web:
	cd apps/web && npm run dev

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".next" -exec rm -rf {} +
