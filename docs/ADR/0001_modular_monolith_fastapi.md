# ADR 0001: Lựa Chọn Kiến Trúc Modular Monolith Dùng FastAPI (Python)

* **Trạng thái:** ACCEPTED
* **Ngày quyết định:** 2026-11-22
* **Người quyết định:** Toàn bộ nhóm phát triển ThinkBuild

---

## Bối Cảnh (Context)

Hệ thống ThinkBuild yêu cầu tích hợp chặt chẽ giữa 3 khối tính năng:
1. RESTful API truyền thống (Quản lý User, Dự án, Task, Bằng chứng, Cổng kiểm soát).
2. Xử lý Trí tuệ Nhân tạo & Machine Learning (Tính toán vector embedding, phân loại văn bản, tìm kiếm độ tương đồng, tính điểm UGI, BKT).
3. Streaming tương tác thời gian thực (SSE cho phiên phản biện AI).

Các phương án kiến trúc được xem xét:
* **Phương án A: Microservices phân tán** (Backend viết bằng Node.js / NestJS, AI Service viết bằng Python FastAPI, kết nối qua gRPC/RabbitMQ).
* **Phương án B: Modular Monolith bằng Python FastAPI** (Gom toàn bộ nghiệp vụ và ML engine vào một codebase có phân chia module rõ ràng; chỉ tách riêng Sandbox thực thi code thành container cô lập).

---

## Quyết Định (Decision)

Nhóm thống nhất chọn **Phương án B: Modular Monolith bằng Python FastAPI**:
* Tách biệt logic theo module (`auth`, `projects`, `tasks`, `gates`, `defense`, `ml_engine`).
* Sử dụng **Python 3.11+** làm ngôn ngữ chủ đạo cho toàn bộ Backend để tận dụng trực tiếp hệ sinh thái ML (`sentence-transformers`, `numpy`, `scikit-learn`, `PyTorch`) mà không phải chịu độ trễ (overhead) do giao tiếp mạng giữa nhiều microservices.
* Tách riêng duy nhất dịch vụ **Code Sandbox** (`apps/sandbox`) thành một container độc lập không có kết nối internet để bảo đảm an ninh hệ thống khi thực thi code do sinh viên nộp.

---

## Hệ Quả (Consequences)

* **Ưu điểm:**
  * Giảm thiểu tối đa độ phức tạp vận hành: Triển khai đơn giản chỉ với 1 Docker container cho API.
  * Hiệu năng cao: Các phép tính vector cosine similarity hoặc phân loại văn bản có thể gọi trực tiếp trong bộ nhớ (in-memory) hoặc qua SQL pgvector.
  * Tiết kiệm thời gian debug và tránh lỗi lệch schema giữa các dịch vụ.
* **Nhược điểm & Biện pháp khắc phục:**
  * Xử lý tác vụ nặng có thể chặn event loop của FastAPI: Khắc phục bằng cách đẩy các tác vụ nặng (như batch embedding) vào Background Tasks hoặc Worker hàng đợi (Arq/Redis).
