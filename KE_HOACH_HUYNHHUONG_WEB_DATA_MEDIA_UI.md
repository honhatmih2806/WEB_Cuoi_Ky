# 🎨 KẾ HOẠCH CÔNG VIỆC — HUỲNH HƯƠNG (WEB TEAM 1)

> **Dự án:** UteTechStore — Cloud-Native E-Commerce & Media Processing  
> **Thành viên:** **HuynhHuong**  
> **Vai trò:** Frontend UI/UX, Product Data Refinement & Cloud Media Gallery (Next.js 14 + Tailwind CSS)  
> **Nhánh Git làm việc:** `feature/web-ui-data-media`  

---

## 🎯 1. Ý Tưởng & Mục Tiêu

Bạn chịu trách nhiệm **tối ưu toàn bộ trải nghiệm nhìn và đọc trên Frontend `UteTechStore`**:
1. **Tinh giản dữ liệu sản phẩm (Ít chữ - Sang trọng - Hiệu quả):** Loại bỏ các combo AI phức tạp và mô tả dài dòng, đưa về chuẩn boutique tối giản.
2. **Xây dựng giao diện Tìm kiếm theo giá & Công cụ Định giá Thu cũ Đổi mới (Trade-in Modal):** Kết nối API mới do **DangKhoa** viết.
3. **Xây dựng giao diện Kho Tài Liệu / Slides & Watermark (`/documents`):** Cho phép upload ảnh sản phẩm hoặc file PDF slide lên Cloud S3, cấu hình watermark và xem Gallery Thumbnail 16:9 trực quan.

---

## 🛠️ 2. Các File Bạn Cần Tạo Mới & Chỉnh Sửa

| Thao tác | Đường dẫn File | Nội dung thực hiện |
| :---: | :--- | :--- |
| **Chỉnh sửa** | `scripts/seed_products.py` | Rút gọn tiêu đề, `brief_desc` (1 câu < 20 từ), `full_desc` (tối đa 2-3 câu), giữ 4-5 `specs` cốt lõi; bỏ các combo AI rườm rà. |
| **Chỉnh sửa** | `apps/web/src/services/fallbackData.ts` | Đồng bộ dữ liệu sản phẩm đã tinh giản từ `seed_products.py` để web chạy offline vẫn chuẩn đẹp. |
| **Chỉnh sửa** | `apps/web/src/app/page.tsx` | Bổ sung bộ lọc khoảng giá nhanh (`Dưới 20tr`, `20 - 50tr`, `Trên 50tr`) truyền `min_price`, `max_price` xuống hàm `fetchProducts` của **DangKhoa**. |
| **Tạo mới** | `apps/web/src/components/TradeInModal.tsx` | Giao diện Modal "Định giá Thu cũ Đổi mới" (chọn dòng máy, tình trạng `99%`/`95%`/`90%`, hiển thị giá thu mua + trợ giá). |
| **Tạo mới** | `apps/web/src/app/documents/page.tsx` | Trang quản lý Tài liệu PDF & Ảnh Watermark trên Cloud (Upload form, tùy chỉnh text/opacity/góc xoay watermark, Gallery Thumbnail 16:9, nút tải về). |
| **Chỉnh sửa** | `apps/web/src/components/Navbar.tsx` | Thêm nút **`Định giá thu cũ`** (mở `TradeInModal`) và link điều hướng **`Tài liệu Cloud`** (tới `/documents`). |

*(Lưu ý: Giữ nguyên phong cách thiết kế sáng `#FFFFFF`/`#F8F9FA`, viền mảnh `#E5E7EB`, không dùng icon thay cho văn bản mô tả nội dung).*

---

## 🚀 3. Hướng Dẫn Triển Khai Chi Tiết

### Bước 1: Mở nhánh Git riêng
```bash
git checkout main
git pull origin main
git checkout -b feature/web-ui-data-media
```

### Bước 2: Tinh giản Data sản phẩm
- Sửa `scripts/seed_products.py`, sau đó chạy lại lệnh nạp DB:
  ```powershell
  .\.venv\Scripts\python.exe scripts/seed_products.py
  ```
- Cập nhật đồng bộ sang `apps/web/src/services/fallbackData.ts`.

### Bước 3: Bổ sung Lọc Giá & Modal Định Giá trên Trang Chủ
- Trong `apps/web/src/app/page.tsx`: thêm state `priceRange` (`minPrice`, `maxPrice`) và truyền vào `fetchProducts({ ..., min_price, max_price })`.
- Trong `apps/web/src/components/TradeInModal.tsx`: tạo form chọn hãng, model, tình trạng máy, gọi hàm `estimateTradeIn(...)` trong `api.ts` và hiển thị bảng giá thu mua + trợ giá rõ ràng.

### Bước 4: Xây dựng trang Cloud Media Gallery (`apps/web/src/app/documents/page.tsx`)
- Form Upload file PDF / ảnh kèm tùy chọn: `watermark_text` (mặc định `"UteTechStore Official"`), `opacity` (`0.1` – `0.8`), `angle` (`-45`, `0`, `45`), `thumbnail_page` (mặc định `1`, có thể chọn `2`).
- Danh sách Gallery hiển thị trạng thái xử lý (`PENDING` / `PROCESSING` / `COMPLETED`), ảnh Thumbnail tỉ lệ `aspect-video` (16:9) lấy URL từ S3/CloudFront và nút tải file đã đóng Watermark.

---

## 🤝 4. Điểm Phối Hợp Với Các Thành Viên Khác

- **Với DangKhoa (Web Backend):** Sử dụng các hàm trong `apps/web/src/services/api.ts` và kiểu dữ liệu `apps/web/src/types/index.ts` do DangKhoa cung cấp (`fetchProducts` có `min_price`/`max_price`, `estimateTradeIn`, `uploadDocument`, `fetchDocuments`).
- **Với NgocHuy & TrongSon (Cloud Team):** Kiểm tra hiển thị URL ảnh trả về từ S3 / LocalStack không bị lỗi CORS hoặc sai domain.

---

## ✅ 5. Tiêu Chí Nghiệm Thu (Definition of Done)

- [ ] Trang chủ hiển thị danh sách sản phẩm gọn gàng, ít chữ, đúng chuẩn thẩm mỹ tối giản.
- [ ] Bộ lọc tìm kiếm theo tên + khoảng giá hoạt động mượt mà với Backend.
- [ ] Modal Định giá Thu cũ Đổi mới tính toán và hiển thị kết quả chính xác.
- [ ] Trang `/documents` upload được PDF/ảnh và hiển thị được Gallery Thumbnail từ API.
- [ ] Chạy `npm run build` tại `apps/web` thành công với 0 lỗi TypeScript.
- [ ] Push code lên nhánh `feature/web-ui-data-media` và tạo Pull Request vào `main`.
