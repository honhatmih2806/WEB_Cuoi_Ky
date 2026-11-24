# 📋 BẢNG PHÂN CÔNG NHIỆM VỤ — THÀNH VIÊN 1

> **Dự Án:** Hệ Thống Thương Mại Điện Tử UteTechStore  
> **Người thực hiện:** Thành viên 1  
> **Trách nhiệm:** Tinh chỉnh, chuẩn hóa toàn bộ dữ liệu hiển thị sản phẩm (Ít chữ, súc tích, đẳng cấp Luxury Minimalist Nhật Bản)  
> **Thời hạn khuyến nghị:** 1 - 2 ngày  

---

## 🎯 1. Mục Tiêu Chính

Hiện tại dữ liệu sản phẩm đang bị **quá nhiều chữ, lan man** (chứa nhiều thuật ngữ kỹ thuật phức tạp, các combo phòng lab AI cồng kềnh và lẫn lộn dữ liệu bài tập cũ). 

Nhiệm vụ của bạn là:
1. **Lược bỏ hoàn toàn những nội dung rườm rà, lan man** (như các gói combo AI lab, máy trạm quá xa vời với người tiêu dùng phổ thông).
2. **Chuẩn hóa danh mục điện tử tiêu dùng cao cấp** theo phong cách tối giản của [techstore.jp](https://techstore.jp/) và Apple Store: **Ít chữ nhưng đắt giá, chuyên nghiệp, thông tin hiển thị gãy gọn và thanh lịch**.
3. **Đồng bộ dữ liệu** vào cả 2 nơi: Cơ sở dữ liệu Backend SQLite (`scripts/seed_products.py`) và Bộ dữ liệu dự phòng Frontend (`apps/web/src/services/fallbackData.ts`).

---

## 🛠️ 2. Các Tệp Tin Bạn Sẽ Làm Việc

1. **File cấu hình nạp CSDL Backend:**  
   `scripts/seed_products.py`
2. **File dữ liệu dự phòng Frontend (Zero-Downtime):**  
   `apps/web/src/services/fallbackData.ts`
3. **Thư mục kiểm tra dọn dẹp:**  
   `data/` (Xóa bỏ hoặc tách riêng các file quiz trắc nghiệm cũ không dùng tới như `seed_gold_web_ai.json`)

---

## 📐 3. Quy Chuẩn Dữ Liệu Mới (Data Standards)

Mỗi sản phẩm phải tuân thủ nghiêm ngặt nguyên tắc **"Ít chữ - Trực diện - Đẳng cấp"**:

| Trường Dữ Liệu | Tiêu Chuẩn Mới (Cần đạt) | Ví Dụ Mẫu |
| :--- | :--- | :--- |
| **Tiêu đề (`title`)** | Ngắn gọn: `[Hãng] + [Tên Model] + [Cấu hình chính]`. Không chèn câu từ quảng cáo. | `Apple MacBook Pro 16" M4 Max 48GB/1TB` |
| **Mã sản phẩm (`sku`)** | Viết hoa, ngắn gọn, chuẩn kho hàng. | `APL-MBP16-M4M` |
| **Mô tả ngắn (`brief_desc`)** | **Đúng 1 câu duy nhất (dưới 20 từ)**, nêu bật điểm mạnh kỹ thuật cốt lõi. | `Chip M4 Max 16-core, màn hình Liquid Retina XDR 120Hz, pin 24 giờ liên tục.` |
| **Mô tả chi tiết (`full_desc`)** | **Tối đa 2 đến 3 câu thanh lịch**, chuẩn xác, không bóng bẩy hay tâng bốc quá đà. | `Thiết kế nhôm Space Black nguyên khối với công nghệ anode hóa chống bám vân tay. Tối ưu cho tác vụ đồ họa chuyên sâu và lập trình chuyên nghiệp.` |
| **Thông số (`specs`)** | **Đúng 4 - 5 thông số kỹ thuật cốt lõi nhất** (dạng Key - Value rõ ràng). | - **Vi xử lý:** Apple M4 Max (16 CPU, 40 GPU)<br>- **Bộ nhớ:** 48GB Unified RAM 546GB/s<br>- **Ổ cứng:** 1TB SSD NVMe 7.4GB/s<br>- **Màn hình:** 16.2" Liquid Retina XDR 120Hz |
| **Nhãn huy hiệu (`badge`)** | 1 nhãn ngắn gọn, viết hoa (1-3 từ). | `M4 MAX`, `TITANIUM`, `HI-RES SOUND`, `OLED 4K` |
| **Giá bán (`price` & `original_price`)** | Giá bán thực tế hợp lý theo thị trường Việt Nam (VNĐ). | Giá gốc: `89.990.000₫`, Giá KM: `84.990.000₫` |
| **Hình ảnh (`thumbnail` & `gallery`)** | Link ảnh sản phẩm chất lượng cao, nền sáng sạch sẽ, rõ nét góc cạnh. | Ảnh Unsplash hoặc CDN chính hãng |

---

## 📂 4. Phân Bổ 6 Nhóm Danh Mục Trọng Tâm

Chỉ tập trung vào 6 - 8 danh mục sản phẩm điện tử cao cấp thiết thực nhất:

1. **Laptops & MacBooks:** MacBook Pro M4, MacBook Air M3, Dell XPS 16, ThinkPad X1 Carbon Gen 12, ASUS ROG Zephyrus G16.
2. **Điện Thoại Flagship:** iPhone 16 Pro Max, Samsung Galaxy S24 Ultra, Google Pixel 9 Pro XL, Sony Xperia 1 VI.
3. **Máy Tính Bảng (Tablets):** iPad Pro 13" M4 Ultra Retina OLED, Galaxy Tab S9 Ultra.
4. **Âm Thanh & Tai Nghe Hi-Fi:** AirPods Max USB-C, Sony WH-1000XM5, Bang & Olufsen Beoplay H95.
5. **Màn Hình Chuyên Nghiệp:** Apple Studio Display 5K, Dell UltraSharp 32" 6K, LG UltraGear OLED 4K.
6. **Đồng Hồ & Phụ Kiện:** Apple Watch Ultra 2, Chuột Logitech MX Master 3S, Bàn phím nhôm Keychron Q1 Max, Cáp Apple Thunderbolt 5 Pro.

*(Lưu ý: Bỏ hoàn toàn các gói combo AI Lab / Rigs phức tạp không cần thiết)*.

---

## 🚀 5. Hướng Dẫn Thực Hiện Từng Bước

### Bước 1: Chỉnh sửa file seed database
Mở file `scripts/seed_products.py`:
- Rà soát danh sách `categories_data` và `products_list`.
- Thay thế các đoạn mô tả dài dòng bằng nội dung súc tích theo bảng quy chuẩn ở Mục 3.
- Xóa bỏ các sản phẩm combo AI lan man.

### Bước 2: Chạy script nạp lại dữ liệu CSDL
Mở terminal tại thư mục gốc và thực thi:
```powershell
# Chạy với môi trường ảo Python đã được cài sẵn
.\.venv\Scripts\python.exe scripts/seed_products.py
```
*(Đảm bảo terminal báo thành công: `✅ Đã tạo thành công ... sản phẩm điện tử cao cấp!`)*

### Bước 3: Cập nhật file dữ liệu Frontend Fallback
Mở file `apps/web/src/services/fallbackData.ts`:
- Sao chép danh sách sản phẩm và danh mục đã chuẩn hóa từ Bước 1 vào mảng `FALLBACK_PRODUCTS` và `FALLBACK_CATEGORIES`.
- Điều này đảm bảo khi người dùng mất kết nối API hoặc chạy độc lập, dữ liệu hiển thị trên web vẫn súc tích, hoàn hảo.

### Bước 4: Kiểm tra trực quan trên trình duyệt
1. Chạy hệ thống bằng cách nhấp vào `run_store.bat` hoặc lệnh:
   ```powershell
   python scripts/start_servers.py
   ```
2. Mở trình duyệt tại [http://localhost:3000](http://localhost:3000).
3. Đánh giá:
   - Các thẻ sản phẩm trên trang chủ có đều đặn, sạch sẽ, không bị dài dòng vỡ khung không?
   - Nhấp vào từng sản phẩm để xem Modal chi tiết: Mô tả và 4-5 gạch đầu dòng thông số có hiển thị tinh tế, dễ đọc không?

---

## ✅ 6. Tiêu Chí Nghiệm Thu (Definition of Done)

- [ ] Toàn bộ 20 - 25 sản phẩm điện tử đều có tên ngắn gọn, mô tả dưới 20 từ.
- [ ] Không còn bất kỳ gói combo AI lab hay thuật ngữ rối rắm nào trên web.
- [ ] Bảng thông số kỹ thuật (`specs`) hiển thị gọn gàng 4 - 5 mục quan trọng nhất.
- [ ] CSDL `titan_silicon.db` đã được nạp lại dữ liệu mới thành công.
- [ ] File `fallbackData.ts` đã được cập nhật đồng bộ với CSDL.
- [ ] Trang web tải nhanh, giao diện thoáng đãng, sang trọng đúng chuẩn Nhật Bản.
