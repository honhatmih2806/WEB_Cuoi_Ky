# 📋 BẢNG PHÂN CÔNG NHIỆM VỤ — THÀNH VIÊN 2

> **Dự Án:** Hệ Thống Thương Mại Điện Tử UteTechStore  
> **Người thực hiện:** Thành viên 2  
> **Trách nhiệm:** Xây dựng Công cụ Định giá sản phẩm & Hoàn thiện Backend Tìm kiếm theo Giá / Tên  
> **Thời hạn khuyến nghị:** 2 - 3 ngày  

---

## 🎯 1. Mục Tiêu Chính

Hiện tại hệ thống:
1. **Tìm kiếm & Lọc theo khoảng giá:** Mới chỉ xử lý giao diện phía Frontend cơ bản, cần hoàn thiện logic Backend API kết nối thực tế với Cơ sở dữ liệu SQLite/PostgreSQL để người dùng có thể tìm kiếm sản phẩm theo từ khóa và lọc theo từng khoảng giá tiền mong muốn.
2. **Công cụ Định giá sản phẩm (Product Valuation / Pricing Tool):** Cần xây dựng mới tính năng định giá giúp người dùng ước tính ngân sách và định giá máy cũ lên đời (Trade-in) — một tính năng chuẩn mực của các hệ thống bán lẻ công nghệ cao cấp như Apple Store hay chuỗi bán lẻ Nhật Bản.

---

## 🛠️ 2. Các Tệp Tin Bạn Sẽ Làm Việc

### Phía Backend (FastAPI / Python):
1. `apps/api/routers/products.py` — Nâng cấp API tìm kiếm, lọc theo khoảng giá `min_price`, `max_price`.
2. `apps/api/routers/pricing.py` — *(Tạo mới)* Router xử lý công cụ định giá thu cũ đổi mới & gợi ý ngân sách.
3. `apps/api/schemas/pricing.py` — *(Tạo mới)* Cấu trúc DTO request & response cho công cụ định giá.
4. `apps/api/main.py` — Đăng ký router `pricing` vào ứng dụng FastAPI.

### Phía Frontend (Next.js / TypeScript):
1. `apps/web/src/services/api.ts` — Bổ sung tham số `min_price`, `max_price` vào hàm gọi `fetchProducts` và viết các hàm gọi API định giá.
2. `apps/web/src/app/page.tsx` — Tích hợp thanh trượt / bộ chọn nhanh khoảng giá (`Price Range Selector`).
3. `apps/web/src/components/TradeInModal.tsx` — *(Tạo mới)* Modal giao diện "Công cụ Định giá Thu cũ Đổi mới".
4. `apps/web/src/components/Navbar.tsx` — Thêm nút bấm mở công cụ "Định giá thu cũ" trên thanh điều hướng.

---

## 🚀 3. Hướng Dẫn Kỹ Thuật Chi Tiết

### NHIỆM VỤ 2.1: Hoàn Thiện Backend Tìm Kiếm Theo Tên & Lọc Khoảng Giá

#### 1. Backend API (`apps/api/routers/products.py`):
Đảm bảo endpoint `GET /api/v1/products` xử lý đầy đủ các query params:
- `query: Optional[str]` — Tìm kiếm không phân biệt hoa thường (`ilike`), hỗ trợ tách nhiều từ khóa (ví dụ: gõ "macbook 16" hoặc "rtx 5090" đều tìm ra chính xác).
- `min_price: Optional[int]` — Lọc giá sản phẩm `>= min_price`.
- `max_price: Optional[int]` — Lọc giá sản phẩm `<= max_price`.
- `sort_by: str` — Hỗ trợ các kiểu sắp xếp:
  - `price_asc`: Giá từ thấp đến cao.
  - `price_desc`: Giá từ cao xuống thấp.
  - `rating`: Đánh giá cao nhất.
  - `newest`: Mới cập nhật.

**Đoạn mã truy vấn mẫu bằng SQLAlchemy trong `products.py`:**
```python
if min_price is not None:
    q = q.filter(Product.price >= min_price)

if max_price is not None:
    q = q.filter(Product.price <= max_price)

if query:
    words = query.strip().split()
    for w in words:
        search_pattern = f"%{w}%"
        q = q.filter(or_(
            Product.title.ilike(search_pattern),
            Product.sku.ilike(search_pattern),
            Product.brief_desc.ilike(search_pattern)
        ))
```

#### 2. Kết nối Frontend (`apps/web/src/services/api.ts` & `page.tsx`):
- Trong `apps/web/src/services/api.ts`, cập nhật hàm `fetchProducts`:
  ```typescript
  export async function fetchProducts(params: {
    brand_slug?: string;
    category_slug?: string;
    query?: string;
    min_price?: number;
    max_price?: number;
    sort_by?: string;
  } = {})
  ```
- Trên giao diện `page.tsx`, thêm thanh bộ lọc khoảng giá nhanh:
  - `Tất cả mức giá`
  - `Dưới 20 triệu` (0 - 20.000.000₫)
  - `Từ 20 - 50 triệu` (20.000.000₫ - 50.000.000₫)
  - `Trên 50 triệu` (50.000.000₫ trở lên)
  - *(Tùy chọn nâng cao: 2 ô nhập giá tối thiểu / tối đa trực tiếp)*.

---

### NHIỆM VỤ 2.2: Xây Dựng Công Cụ Định Giá Sản Phẩm (Pricing & Trade-in Tools)

Bạn sẽ xây dựng **Công cụ Định Giá Thu Cũ Đổi Mới (Trade-in Valuation Calculator)** — khách hàng kiểm tra xem chiếc máy hiện tại của mình được thu mua lại bao nhiêu tiền để bù trừ khi mua máy mới.

#### 1. Xây dựng DTO Backend (`apps/api/schemas/pricing.py`):
```python
from pydantic import BaseModel, Field
from typing import Optional, List

class TradeInRequest(BaseModel):
    category: str = Field(..., description="smartphone, laptop, tablet, smartwatch")
    brand: str = Field(..., description="apple, samsung, dell, sony...")
    model_name: str = Field(..., description="Tên model máy cũ, ví dụ: iPhone 14 Pro Max 256GB")
    condition: str = Field(..., description="grade_a (99%), grade_b (95%), grade_c (90%)")
    storage_capacity: Optional[str] = None
    accessories_included: bool = True

class TradeInEstimateResponse(BaseModel):
    model_name: str
    base_estimated_value: int = Field(..., description="Giá trị định giá máy cũ (VNĐ)")
    trade_in_bonus: int = Field(..., description="Trợ giá lên đời độc quyền từ UteTechStore (VNĐ)")
    total_deduction: int = Field(..., description="Tổng số tiền được trừ khi mua sản phẩm mới (VNĐ)")
    recommendations: List[str] = Field(default=[], description="Các sản phẩm mới phù hợp để lên đời")
```

#### 2. Xây dựng Logic Định Giá Backend (`apps/api/routers/pricing.py`):
- Viết thuật toán tính giá dựa trên cấu hình và tình trạng máy:
  - Máy Grade A (Đẹp như mới 99%): 100% mức giá cơ sở thị trường.
  - Máy Grade B (Trầy xước nhẹ 95%): 85% mức giá cơ sở.
  - Máy Grade C (Cũ theo thời gian 90%): 70% mức giá cơ sở.
  - **Chính sách trợ giá UteTechStore:** Tặng thêm **1.000.000₫ - 2.000.000₫** trợ giá thu cũ đổi mới.
- Cung cấp endpoint: `POST /api/v1/pricing/trade-in-estimate`.

#### 3. Tạo Giao Diện Định Giá Frontend (`apps/web/src/components/TradeInModal.tsx`):
- Thiết kế Modal popup giao diện sáng, tối giản:
  1. **Bước 1:** Chọn thiết bị (iPhone, MacBook, iPad, Laptop...).
  2. **Bước 2:** Chọn tình trạng máy (99% / 95% / 90%).
  3. **Bước 3:** Nhấn **"Định Giá Ngay"** -> Hiển thị kết quả:
     - Giá trị máy cũ thu mua: `XX.000.000₫`
     - Trợ giá UteTechStore: `+1.500.000₫`
     - **Tổng giá trị khấu trừ:** `YY.000.000₫`
     - Nút kêu gọi hành động: **"Áp Dụng Vào Giỏ Hàng Lên Đời"** (tự động tạo voucher giảm giá khấu trừ vào giỏ hàng).

---

## 🧪 4. Hướng Dẫn Kiểm Thử (Testing)

1. **Kiểm thử Swagger API Backend:**
   - Mở [http://localhost:8000/docs](http://localhost:8000/docs).
   - Kiểm tra endpoint `GET /api/v1/products`: Nhập `min_price=20000000`, `max_price=50000000`, `query=MacBook` và nhấn Execute. Kiểm tra kết quả trả về đúng dữ liệu.
   - Kiểm tra endpoint `POST /api/v1/pricing/trade-in-estimate`: Gửi thử JSON định giá máy cũ và nhận về số tiền chuẩn xác.

2. **Kiểm thử Giao diện Web Frontend:**
   - Mở [http://localhost:3000](http://localhost:3000).
   - Gõ từ khóa tìm kiếm vào ô Search Bar trên trang chủ -> Danh sách sản phẩm lập tức cập nhật tương ứng.
   - Chọn bộ lọc khoảng giá (ví dụ: Dưới 20 triệu) -> Chỉ các sản phẩm thỏa mãn hiển thị.
   - Nhấp vào nút **"Định giá thu cũ"** -> Modal hiện lên, nhập thông tin máy cũ, bấm định giá và xem kết quả trực quan.

---

## ✅ 5. Tiêu Chí Nghiệm Thu (Definition of Done)

- [ ] API `GET /api/v1/products` lọc chính xác 100% theo `min_price`, `max_price` và `query`.
- [ ] Frontend có bộ lọc khoảng giá trực quan, bấm lọc là gọi backend tải lại dữ liệu chuẩn.
- [ ] API `POST /api/v1/pricing/trade-in-estimate` hoạt động ổn định, có tài liệu Swagger đầy đủ.
- [ ] Giao diện Modal Định giá thu cũ hoạt động mượt mà, tính toán số tiền rõ ràng, thiết kế sang trọng chuẩn phong cách Nhật Bản.
- [ ] Không có lỗi console hay crash server khi tìm kiếm không ra kết quả.
