# API_CONTRACT.md — Titan Silicon RESTful API Contract

> **Base URL:** `/api/v1`  
> **Cơ chế phản hồi chuẩn (Envelope Response):**
> Tất cả các phản hồi từ API đều tuân thủ cấu trúc đồng nhất:
> ```json
> {
>   "success": true,
>   "data": { ... },
>   "meta": { "total": 10, "page": 1, "page_size": 20 },
>   "error": null
> }
> ```
> Khi xảy ra lỗi:
> ```json
> {
>   "success": false,
>   "data": null,
>   "meta": null,
>   "error": {
>     "code": "ERR_PROD_001",
>     "message": "Không tìm thấy sản phẩm yêu cầu",
>     "details": { "slug": "iphone-18-pro-max" }
>   }
> }
> ```

---

## 1. Danh Mục & Thương Hiệu (`/categories`, `/brands`)

### 1.1. `GET /api/v1/categories`
* **Mô tả:** Lấy danh sách toàn bộ danh mục sản phẩm kèm số lượng sản phẩm.
* **Response (200):**
  ```json
  {
    "success": true,
    "data": [
      {
        "id": "c1...",
        "name": "Apple iPhone",
        "slug": "iphone",
        "icon": "Smartphone",
        "product_count": 6
      },
      {
        "id": "c2...",
        "name": "NVIDIA GeForce & AI",
        "slug": "nvidia-gpu",
        "icon": "Cpu",
        "product_count": 6
      },
      {
        "id": "c3...",
        "name": "Combo Sáng Tạo AI (Bundles)",
        "slug": "bundles",
        "icon": "Sparkles",
        "product_count": 3
      }
    ]
  }
  ```

### 1.2. `GET /api/v1/brands`
* **Mô tả:** Lấy danh sách thương hiệu (`Apple`, `NVIDIA`, `Titan Ecosystem`).

---

## 2. Sản Phẩm (`/products`)

### 2.1. `GET /api/v1/products`
* **Query Parameters:**
  * `brand_slug` (string, optional): Lọc theo hãng (`apple`, `nvidia`, `titan`).
  * `category_slug` (string, optional): Lọc theo danh mục.
  * `query` (string, optional): Tìm kiếm theo tên sản phẩm hoặc thông số.
  * `is_featured` (boolean, optional): Lọc sản phẩm nổi bật.
  * `is_bundle` (boolean, optional): Lọc combo độc quyền.
  * `min_price` (integer, optional): Giá tối thiểu (VNĐ).
  * `max_price` (integer, optional): Giá tối đa (VNĐ).
  * `sort_by` (string, default: `newest`): `price_asc`, `price_desc`, `rating`, `newest`.
  * `page` (integer, default: 1).
  * `page_size` (integer, default: 20).

### 2.2. `GET /api/v1/products/{slug}`
* **Mô tả:** Lấy thông tin chi tiết một sản phẩm theo slug, kèm theo bảng thông số kỹ thuật đầy đủ (`specifications`), ảnh thư viện (`gallery`), và danh sách đánh giá (`reviews`).

---

## 3. Combo Tích Hợp Độc Quyền (`/bundles`)

### 3.1. `GET /api/v1/bundles`
* **Mô tả:** Lấy danh sách các gói kết hợp iPhone + NVIDIA GPU dành cho Studio, AI Research, và Gaming.
* **Chi tiết gồm:** Danh sách linh kiện thành phần, tổng giá gốc, giá ưu đãi combo, % tiết kiệm được.

---

## 4. Trợ Lý Tư Vấn Cấu Hình AI (`/advisor`)

### 4.1. `POST /api/v1/advisor/recommend`
* **Body:**
  ```json
  {
    "use_case": "AI_RESEARCH_LLM", // DEEP_LEARNING, 4K_PRORES_CINEMA, GAMING_STREAMING, MOBILE_EDGE_AI
    "budget_range": "HIGH",        // MID (40-60tr), HIGH (70-100tr), ULTRA (>100tr)
    "primary_focus": "BOTH"         // IPHONE, NVIDIA, BOTH
  }
  ```
* **Response (200):**
  * Trả về cấu hình iPhone và NVIDIA GPU tương thích tối ưu nhất, điểm hiệu năng mô phỏng (AI TOPS, Benchmark, VRAM capacity), và lý do kỹ thuật chi tiết tại sao combo này sinh ra để dành cho người dùng.

---

## 5. Đơn Hàng & Thanh Toán (`/orders`)

### 5.1. `POST /api/v1/orders/checkout`
* **Body:**
  ```json
  {
    "customer_name": "Nguyễn Hoàng Nam",
    "customer_email": "hoangnam@gmail.com",
    "customer_phone": "0988776655",
    "shipping_address": "Tòa Landmark 81, P.22, Q. Bình Thạnh, TP. Hồ Chí Minh",
    "payment_method": "BANKING_QR", // COD, BANKING_QR, INSTALLMENT_0
    "voucher_code": "TITANVIP",
    "notes": "Giao giờ hành chính, gọi trước 15 phút",
    "items": [
      {
        "product_id": "...",
        "quantity": 1
      }
    ]
  }
  ```
* **Response (201):**
  * `order_code` (VD: `ORD-2026-98124`)
  * `final_amount`: Tổng tiền thực tế đã áp voucher
  * `qr_payment_data`: Thông tin chuyển khoản VietQR tự sinh nếu chọn phương thức chuyển khoản.

### 5.2. `GET /api/v1/orders/track/{order_code}`
* **Mô tả:** Tra cứu tiến độ đơn hàng và thời gian giao dự kiến.
