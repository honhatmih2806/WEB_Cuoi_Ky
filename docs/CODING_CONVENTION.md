# CODING_CONVENTION.md — Titan Silicon Coding Standards

## 1. Backend (Python & FastAPI)
- **Kiến trúc:** Phân tầng tách biệt `core/` (config, envelope, db), `models/` (SQLAlchemy entities), `schemas/` (Pydantic DTOs), `routers/` (FastAPI controllers).
- **Phản hồi API:** Luôn bọc qua `ApiResponse.ok(...)` hoặc ném ngoại lệ `AppException(...)` để trả về đúng format Envelope.
- **Xử lý số tiền:** Mọi giá trị tiền tệ trong DB lưu bằng kiểu `BigInteger` (đơn vị VNĐ, không lưu float để tránh lỗi làm tròn).
- **Kiểu dữ liệu:** Sử dụng Type Hints 100% trong toàn bộ hàm và schemas.

## 2. Frontend (Next.js & TypeScript & Tailwind CSS)
- **App Router:** Tận dụng Next.js 14 App Router, Client Component đánh dấu `'use client';` rõ ràng khi có tương tác state.
- **Phong cách UI:**
  - Dark Titanium mode chủ đạo kết hợp ánh sáng Cyber-Green (`#76B900`).
  - Sử dụng Tailwind CSS utility classes, tránh CSS thuần phân tán.
  - Các icon sử dụng từ thư viện `lucide-react`.
- **Formatting tiền tệ:** Format hiển thị dạng `34.990.000 ₫` hoặc viết hoa ngắn gọn `34.99 triệu ₫`.
