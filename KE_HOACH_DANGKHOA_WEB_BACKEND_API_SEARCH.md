# ⚙️ KẾ HOẠCH CÔNG VIỆC — ĐĂNG KHOA (WEB TEAM 2)

> **Dự án:** UteTechStore — Cloud-Native E-Commerce & Media Processing  
> **Thành viên:** **DangKhoa**  
> **Vai trò:** Backend API, Search/Pricing Engine & Cloud Integration Bridge (FastAPI + SQLAlchemy + TypeScript API Client)  
> **Nhánh Git làm việc:** `feature/web-backend-search-pricing`  

---

## 🎯 1. Ý Tưởng & Mục Tiêu

Bạn là cầu nối kỹ thuật quan trọng nhất giữa **Frontend (`HuynhHuong`)** và **Cloud (`NgocHuy` & `TrongSon`)**:
1. **Hoàn thiện Backend Tìm kiếm theo tên & Lọc theo khoảng giá** cho danh mục sản phẩm.
2. **Xây dựng Backend API Công cụ Định giá sản phẩm** (Thu cũ đổi mới & Gợi ý theo ngân sách).
3. **Xây dựng Router & Entity Quản lý Tài liệu / Slides Cloud (`/api/v1/documents`):** Tiếp nhận file upload từ Frontend, gọi `s3_service.py` của **NgocHuy** để đẩy lên S3, và lưu metadata vào Database (`documents`).
4. **Cập nhật tầng `api.ts` & `types/index.ts` trên Frontend** để **HuynhHuong** chỉ việc gọi hàm dùng ngay.

---

## 🛠️ 2. Các File Bạn Cần Tạo Mới & Chỉnh Sửa

| Thao tác | Đường dẫn File | Nội dung thực hiện |
| :---: | :--- | :--- |
| **Chỉnh sửa** | `apps/api/routers/products.py` | Nâng cấp `query` hỗ trợ tìm nhiều từ khóa (`words = query.strip().split()`), lọc `min_price`, `max_price` và sắp xếp chuẩn xác. |
| **Tạo mới** | `apps/api/schemas/pricing.py` | Tạo Pydantic DTO: `TradeInRequest`, `TradeInEstimateResponse`, `BudgetAdvisorResponse`. |
| **Tạo mới** | `apps/api/routers/pricing.py` | Tạo endpoints `POST /api/v1/pricing/trade-in-estimate` và `GET /api/v1/pricing/budget-advisor`. |
| **Chỉnh sửa** | `apps/api/models/entities.py` | Thêm Entity `SlideDocument` (`__tablename__ = "documents"`) lưu metadata tài liệu & URL Thumbnail/PDF từ S3. |
| **Tạo mới** | `apps/api/routers/documents.py` | Tạo endpoints `/api/v1/documents/upload`, `/api/v1/documents` (tìm kiếm + phân trang), `/api/v1/documents/{doc_id}` gọi `s3_service.py`. |
| **Chỉnh sửa** | `apps/api/main.py` | Đăng ký `pricing.router` và `documents.router` với prefix `settings.API_V1_STR`. |
| **Chỉnh sửa** | `apps/web/src/types/index.ts` | Thêm interface `TradeInRequest`, `TradeInResult`, `SlideDocument`. |
| **Chỉnh sửa** | `apps/web/src/services/api.ts` | Cập nhật `fetchProducts` nhận `min_price`, `max_price`; thêm `estimateTradeIn()`, `uploadDocument()`, `fetchDocuments()`. |

---

## 🚀 3. Hướng Dẫn Triển Khai Chi Tiết

### Bước 1: Mở nhánh Git riêng
```bash
git checkout main
git pull origin main
git checkout -b feature/web-backend-search-pricing
```

### Bước 2: Nâng cấp Tìm kiếm & Lọc giá (`apps/api/routers/products.py`)
- Trong `get_products(...)`, tách `query` thành từng từ khóa để tìm không phân biệt hoa thường trên `Product.title`, `Product.sku`, `Product.brief_desc`:
  ```python
  if query:
      for word in query.strip().split():
          pattern = f"%{word}%"
          q = q.filter(or_(
              Product.title.ilike(pattern),
              Product.sku.ilike(pattern),
              Product.brief_desc.ilike(pattern)
          ))
  ```
- Đảm bảo `min_price` và `max_price` kết hợp mượt với `brand_slug`, `category_slug`, `sort_by` và `MetaPagination`.

### Bước 3: Xây dựng Công cụ Định giá (`apps/api/routers/pricing.py`)
- **`POST /api/v1/pricing/trade-in-estimate`:** Tính giá trị máy cũ theo `category`, `brand`, `model_name`, `condition` (`grade_a`: 100%, `grade_b`: 85%, `grade_c`: 70% giá cơ sở) + trợ giá lên đời từ `UteTechStore`, trả về `ApiResponse.ok(...)`.
- **`GET /api/v1/pricing/budget-advisor`:** Nhận `max_budget` và `category_slug`, truy vấn các sản phẩm có `Product.price <= max_budget` sắp xếp theo đánh giá và hiệu năng/giá tốt nhất.

### Bước 4: Xây dựng Cloud Documents Bridge (`apps/api/routers/documents.py`)
- Endpoint `POST /api/v1/documents/upload`:
  - Kiểm tra định dạng file (`.pdf`, `.png`, `.jpg`, `.webp`), ném `AppException` nếu file không hợp lệ.
  - Tạo bản ghi `SlideDocument` với trạng thái `PENDING`.
  - Gọi `s3_service.upload_raw_file(...)` của **NgocHuy** đẩy file lên S3 `raw/` (hoặc chạy `BackgroundTasks` xử lý cục bộ nếu chưa bật LocalStack).
  - Trả về `ApiResponse.ok(data=doc_dto)`.
- Endpoint `GET /api/v1/documents`: Hỗ trợ tìm kiếm theo `title` / `topics` và phân trang chuẩn `MetaPagination`.

---

## 🤝 4. Điểm Phối Hợp Với Các Thành Viên Khác

- **Với NgocHuy (Cloud 1):** Thống nhất interface của `apps/api/services/s3_service.py` để gọi upload và lấy URL từ S3/CloudFront.
- **Với HuynhHuong (Web 1):** Cung cấp sẵn các hàm trong `apps/web/src/services/api.ts` và kiểu dữ liệu trong `apps/web/src/types/index.ts`, đồng thời test kỹ trên Swagger (`http://localhost:8000/api/v1/docs`) trước khi HuynhHuong nối vào UI.

---

## ✅ 5. Tiêu Chí Nghiệm Thu (Definition of Done)

- [ ] `GET /api/v1/products` lọc chính xác theo `query` nhiều từ khóa, `min_price`, `max_price`.
- [ ] `POST /api/v1/pricing/trade-in-estimate` và `GET /api/v1/pricing/budget-advisor` hoạt động chuẩn trên Swagger Docs.
- [ ] `POST /api/v1/documents/upload` và `GET /api/v1/documents` trả về đúng chuẩn `ApiResponse` & `MetaPagination`.
- [ ] `apps/web/src/services/api.ts` truyền đầy đủ `min_price`, `max_price` và có đủ hàm gọi API mới cho Frontend.
- [ ] Push code lên nhánh `feature/web-backend-search-pricing` và tạo Pull Request vào `main`.
