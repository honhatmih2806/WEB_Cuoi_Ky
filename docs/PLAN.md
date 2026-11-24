# PLAN.md — Lộ Trình Triển Khai Chi Tiết Từ M0 Đến M8

Kế hoạch phát triển dự án ThinkBuild được chia thành 9 mốc nghiêm ngặt. Mỗi mốc có tiêu chí hoàn thành (Definition of Done) rõ ràng và chỉ được chuyển sang mốc tiếp theo khi đã vượt qua toàn bộ tiêu chí kiểm thử.

---

## Bảng Tiến Độ Tổng Thể

| Mốc | Tên Giai Đoạn | Trọng Tâm Kỹ Thuật | Tiêu Chí Hoàn Thành (DoD) |
| :---: | :--- | :--- | :--- |
| **M0** | **Xác minh Dataset & Benchmark** | Kiểm tra giấy phép, làm sạch dữ liệu, benchmark 3 model embedding tiếng Việt | Báo cáo M0, bảng so sánh embedding, ADR được duyệt |
| **M1** | **Monorepo & Hạ Tầng Cốt Lõi** | Khởi tạo repo, Docker Compose, Postgres + pgvector, Redis, MinIO, Auth JWT | `docker compose up` 1 lệnh xanh toàn bộ, health check đạt 100% |
| **M2** | **Gold Pipeline & Ingest** | Viết script nạp dữ liệu từ PrepMaster + Imbue, loại trùng lặp ngữ nghĩa | Gold Dataset v0 có tối thiểu 200 câu hỏi chuẩn được duyệt |
| **M3** | **ML Engine (Dual-Dataset)** | Xây dựng pipeline Embedding, Classifier (F1), Vector Search, Rerank, Mapping | Macro-F1 > 0.82; hit@3 > 88% trên tập test kiểm thử |
| **M4** | **Onboarding & Sinh Lộ Trình** | Xây dựng LLM Gateway (structured output) phân tích prompt thành Phase/Task | Nhập đề tài Web + AI sinh ra 5 phase và 15 task chuẩn schema |
| **M5** | **Hệ Thống Cổng & Sandbox** | Hoàn thiện 3 tầng test: Kiến thức, Code Comprehension qua Sandbox, Phản biện | Sinh viên qua được 3 test mới mở phase kế; sandbox an toàn |
| **M6** | **Dual-Dataset Engine & Review UI** | Vòng lặp đối chiếu Generated và Gold, cơ chế 4 quan hệ (reinforce, conflict...) | Không bao giờ ghi đè Gold tự động; Review Queue chạy mượt |
| **M7** | **Bảng Điều Khiển & Chỉ Số UGI** | Trực quan hóa Radar Chart, tính toán công thức UGI, phiên phản biện cuối cùng | Demo hoàn chỉnh luồng từ Onboarding đến Bảo vệ đồ án |
| **M8** | **Thực Nghiệm & Báo Cáo Hackathon** | Thử nghiệm so sánh nhóm dùng ThinkBuild vs ChatGPT thuần (H1 - H4) | Báo cáo thực nghiệm khoa học, slide thuyết trình, video backup |

---

## Chi Tiết Nhiệm Vụ Từng Mốc

### Mốc M0: Xác Minh Dataset & Chuẩn Bị Dữ Liệu
* Tải và kiểm tra giấy phép MIT của `imbue/code-comprehension` và các tập trắc nghiệm phỏng vấn.
* Trích xuất mẫu ngẫu nhiên 100 câu hỏi tiếng Việt + tiếng Anh.
* Chạy thử nghiệm embedding: So sánh `BAAI/bge-m3` và `intfloat/multilingual-e5-base` về tốc độ và độ chính xác phân cụm.

### Mốc M1: Thiết Lập Hạ Tầng (Infrastructure Setup)
* Hoàn thiện `docker-compose.yml` tích hợp `pgvector/pgvector:pg16`, `redis:7-alpine`, `minio/minio`.
* Tạo database schema và migration ban đầu qua SQLAlchemy/Alembic.
* Cài đặt middleware CORS, Exception Handler với envelope `{ success, data, error }`.

### Mốc M2: Nạp & Chuẩn Hóa Gold Dataset
* Xây dựng script `scripts/ingest_gold.py` chuyển đổi câu hỏi trắc nghiệm và cloze/eval code vào bảng `gold_items`.
* Tính toán và lưu trước vector embedding `vector(1024)` cho toàn bộ tập Gold.
* Tạo chỉ mục HNSW trên PostgreSQL: `CREATE INDEX ON gold_items USING hnsw (embedding vector_cosine_ops)`.

### Mốc M3: Xây Dựng Bộ Máy ML & Ánh Xạ
* Xây dựng bộ phân loại `ml/classifiers/` gán nhãn `skill`, `phase`, `type` dựa trên TF-IDF + Logistic Regression hoặc Linear SVM.
* Xây dựng engine tính Cosine Similarity và Cross-encoder rerank để tìm kiếm top-3 mục Gold gần nhất với từng câu hỏi sinh ra.

### Mốc M4: Onboarding & Sinh Lộ Trình Dự Án
* Viết Prompt Template cho LLM Gateway với cơ chế Pydantic Structured Output (ép kiểu JSON chuẩn).
* Tạo cơ chế retry tự động tối đa 3 lần và fallback chain khi một model gặp sự cố.

### Mốc M5: Ba Tầng Kiểm Tra Cổng Giai Đoạn
* Tầng 1: Lấy ngẫu nhiên câu hỏi MCQ từ Gold.
* Tầng 2: Gửi đoạn code và đáp án sinh viên vào dịch vụ Sandbox độc lập (`apps/sandbox`) để chạy thực nghiệm và kiểm tra tính đúng đắn.
* Tầng 3: AI đóng vai Giám khảo, hỏi phản biện trực tiếp qua giao thức Server-Sent Events (SSE).

### Mốc M6: Vòng Lặp Dual-Dataset & Hàng Đợi Duyệt
* Tự động gán quan hệ: `reinforce` (bổ trợ), `conflict` (mâu thuẫn), `extend` (mở rộng), `new` (mới).
* Các mục `conflict` tự động đẩy vào bảng `review_queue` để Giảng viên/Admin click duyệt hoặc loại bỏ.

### Mốc M7: Dashboard, UGI & Phiên Bảo Vệ
* Tính toán công thức chỉ số `UGI`. Cảnh báo đỏ nếu sinh viên hoàn thành task nhanh nhưng điểm test code thấp.
* Vẽ Radar Chart năng lực 6 trục kỹ năng.

### Mốc M8: Đánh Giá Thực Nghiệm & Hoàn Thiện
* Chạy thử nghiệm mù trên 2 nhóm sinh viên (Nhóm A dùng ChatGPT thuần, Nhóm B dùng ThinkBuild).
* Thu thập số liệu điểm thi bảo vệ, đo lường sự khác biệt có ý nghĩa thống kê ($p < 0.05$).
