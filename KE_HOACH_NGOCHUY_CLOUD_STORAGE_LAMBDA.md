# ☁️ KẾ HOẠCH CÔNG VIỆC — NGỌC HUY (CLOUD TEAM 1)

> **Dự án:** UteTechStore — Cloud-Native E-Commerce & Media Processing  
> **Thành viên:** **NgocHuy**  
> **Vai trò:** Cloud Storage & Serverless Processing Engineer (Amazon S3 + AWS Lambda Thumbnail/Watermark)  
> **Nhánh Git làm việc:** `feature/cloud-s3-lambda`  

---

## 🎯 1. Ý Tưởng & Mục Tiêu

Thay vì lưu ảnh sản phẩm và tài liệu PDF cục bộ hoặc phụ thuộc link ngoài, bạn sẽ phụ trách phần **Lưu trữ đám mây (Module 7: S3)** và **Xử lý phi máy chủ bất đồng bộ (Module 6: AWS Lambda)**:
1. Thiết lập **S3 Bucket** (`utetechstore-assets`) phân tách 2 vùng: `raw/` (ảnh/PDF gốc) và `processed/` (Thumbnail 16:9 & PDF đã đóng dấu Watermark `UteTechStore`).
2. Viết **AWS Lambda Function (Python)** tự động kích hoạt khi có file mới vào `raw/` để:
   - Sinh Thumbnail 3 kích thước (`320×180`, `640×360`, `1280×720`) bằng `Pillow` / `PyMuPDF`.
   - Đóng Watermark chữ hoặc logo lên ảnh Thumbnail và toàn bộ trang PDF.
3. Cung cấp service **`s3_service.py`** trong FastAPI (`boto3`) để team Web (**DangKhoa**) gọi upload và lấy URL hiển thị lên Frontend (**HuynhHuong**).

---

## 🛠️ 2. Các File Bạn Cần Tạo Mới & Chỉnh Sửa

| Thao tác | Đường dẫn File | Nội dung thực hiện |
| :---: | :--- | :--- |
| **Tạo mới** | `cloud/lambda_watermark/handler.py` | Code AWS Lambda đọc sự kiện S3, render Thumbnail & đóng Watermark bằng `Pillow` + `PyMuPDF` (`fitz`). |
| **Tạo mới** | `cloud/lambda_watermark/requirements.txt` | Khai báo `pymupdf`, `pillow`, `boto3` cho Lambda Layer / LocalStack. |
| **Tạo mới** | `apps/api/services/s3_service.py` | Lớp wrapper dùng `boto3` để upload file lên S3 (`raw/`), kiểm tra file ở `processed/` và tạo URL/Presigned URL. |
| **Chỉnh sửa** | `apps/api/core/config.py` | Bổ sung cấu hình `AWS_REGION`, `AWS_S3_BUCKET`, `AWS_ENDPOINT_URL` (hỗ trợ cả AWS thật và LocalStack), `CLOUDFRONT_DOMAIN`. |
| **Chỉnh sửa** | `apps/api/requirements.txt` | Thêm `boto3>=1.34.0`, `pillow>=10.0.0`, `pymupdf>=1.24.0`. |

*(Lưu ý: Không sửa trực tiếp các router của DangKhoa hay UI của HuynhHuong để tránh xung đột Git).*

---

## 🚀 3. Hướng Dẫn Triển Khai Chi Tiết

### Bước 1: Mở nhánh Git riêng & cài thư viện
```bash
git checkout main
git pull origin main
git checkout -b feature/cloud-s3-lambda
```

### Bước 2: Bổ sung biến cấu hình AWS vào `apps/api/core/config.py`
Trong class `Settings` tại `apps/api/core/config.py`, thêm các thuộc tính:
```python
    # AWS Cloud / LocalStack Configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-southeast-1")
    AWS_S3_BUCKET: str = os.getenv("AWS_S3_BUCKET", "utetechstore-assets")
    AWS_ENDPOINT_URL: str = os.getenv("AWS_ENDPOINT_URL", "")  # Để trống nếu dùng AWS thật; http://localstack:4566 nếu chạy Docker LocalStack
    CLOUDFRONT_DOMAIN: str = os.getenv("CLOUDFRONT_DOMAIN", "")
```

### Bước 3: Viết `apps/api/services/s3_service.py`
- Khởi tạo `boto3.client("s3", region_name=settings.AWS_REGION, endpoint_url=settings.AWS_ENDPOINT_URL or None)`.
- Viết 3 hàm chuẩn để **DangKhoa** gọi từ `routers/documents.py`:
  1. `upload_raw_file(file_bytes: bytes, key: str, content_type: str) -> str`
  2. `get_public_or_presigned_url(key: str, expires_in: int = 3600) -> str` (ưu tiên `CLOUDFRONT_DOMAIN` nếu đã cấu hình ở Module 5).
  3. `delete_object(key: str) -> bool`

### Bước 4: Viết Lambda Handler (`cloud/lambda_watermark/handler.py`)
- Nhận `event` từ S3 (`Records[0].s3.bucket.name` và `object.key`).
- Chỉ xử lý khi key bắt đầu bằng `raw/`.
- Nếu là `.pdf`: dùng `fitz.open(stream=...)` trích xuất `title`, `page_count`, `topics` (trang 2), render trang chỉ định (mặc định trang 1, hỗ trợ trang 2 nếu trang 1 ít chữ) ra ảnh Thumbnail `sm`/`md`/`lg` và đóng watermark lên toàn bộ các trang PDF.
- Nếu là ảnh sản phẩm (`.jpg`/`.png`/`.webp`): dùng `Pillow` resize đúng tỉ lệ và đóng chữ/logo `UteTechStore` ở góc hoặc chéo giữa ảnh.
- Ghi kết quả ra `processed/thumbnails/...` và `processed/watermarked_pdfs/...`.

---

## 🤝 4. Điểm Phối Hợp Với Các Thành Viên Khác

- **Với TrongSon (Cloud 2):** Cung cấp `cloud/lambda_watermark/handler.py` để TrongSon cấu hình tự động deploy vào LocalStack (`init-aws.sh`) hoặc AWS Lambda + IAM Role đọc/ghi `utetechstore-assets`.
- **Với DangKhoa (Web Backend):** Chốt tên hàm và chữ ký tham số của `s3_service.py` để DangKhoa gọi trực tiếp trong `routers/documents.py`.

---

## ✅ 5. Tiêu Chí Nghiệm Thu (Definition of Done)

- [ ] `apps/api/core/config.py` nhận cấu hình AWS S3 & LocalStack linh hoạt qua biến môi trường.
- [ ] `apps/api/services/s3_service.py` upload được file vào `raw/` và trả về URL truy cập hợp lệ.
- [ ] `cloud/lambda_watermark/handler.py` xử lý thành công cả ảnh sản phẩm lẫn file PDF nhiều trang (giữ được searchable text, không ghi đè file gốc).
- [ ] Push code lên nhánh `feature/cloud-s3-lambda` và tạo Pull Request vào `main`.
