# ERROR_CODES.md — Titan Silicon Error Standards

Hệ thống mã lỗi chuẩn hóa phân tầng theo mã `ERR_<DOMAIN>_<SEQ>`:

| Mã Lỗi | HTTP Code | Mô Tả Ngữ Nghĩa | Hướng Xử Lý Khuyến Nghị |
| :--- | :---: | :--- | :--- |
| **`ERR_PROD_001`** | 404 | Sản phẩm không tồn tại trong hệ thống | Kiểm tra lại slug hoặc id sản phẩm |
| **`ERR_PROD_002`** | 400 | Sản phẩm đã hết hàng trong kho | Thông báo khách chọn cấu hình khác |
| **`ERR_CAT_001`** | 404 | Không tìm thấy danh mục yêu cầu | Kiểm tra slug danh mục |
| **`ERR_CART_001`** | 400 | Giỏ hàng rỗng, không thể tạo đơn | Thêm ít nhất 1 sản phẩm vào giỏ |
| **`ERR_CART_002`** | 400 | Số lượng yêu cầu vượt quá tồn kho khả dụng | Giảm số lượng đặt hàng |
| **`ERR_ORD_001`** | 404 | Mã đơn hàng không tồn tại | Kiểm tra lại mã vận đơn |
| **`ERR_ORD_002`** | 422 | Dữ liệu giao hàng không hợp lệ (email, số điện thoại) | Nhập đúng định dạng số điện thoại Việt Nam |
| **`ERR_VOC_001`** | 400 | Mã giảm giá không hợp lệ hoặc đã hết hạn | Nhập mã khác hoặc để trống |
| **`ERR_SYS_001`** | 500 | Lỗi kết nối cơ sở dữ liệu | Kiểm tra service database |
| **`ERR_SYS_002`** | 500 | Lỗi hệ thống nội bộ không xác định | Liên hệ ban quản trị kỹ thuật |
