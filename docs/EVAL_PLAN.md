# EVAL_PLAN.md — Kế Hoạch Đánh Giá & Kiểm Chứng Thực Nghiệm

Tài liệu này xác định 4 giả thuyết khoa học (H1, H2, H3, H4) nhằm cung cấp số liệu thực tế thuyết phục Hội đồng Giám khảo khi bảo vệ sản phẩm.

---

## 1. Bốn Giả Thuyết Khoa Học Cần Chứng Minh

### Giả thuyết H1: Nâng cao năng lực bảo vệ thực chất
* **Mệnh đề:** Sinh viên sử dụng ThinkBuild đạt điểm số cao hơn trong bài bảo vệ mù (Blind Defense - người chấm không biết sinh viên dùng công cụ gì) so với nhóm chỉ sử dụng ChatGPT thông thường.
* **Phương pháp đo:** Thử nghiệm ngẫu nhiên có đối chứng trên 2 nhóm (mỗi nhóm 15 - 20 sinh viên) làm cùng một đề tài trong 1 tuần:
  * Nhóm Đối chứng (Control Group): Làm tự do kết hợp ChatGPT thông thường.
  * Nhóm Thực nghiệm (Treatment Group): Làm qua hệ thống ThinkBuild (bắt buộc qua 3 cổng test).
* **Chỉ số:** So sánh điểm bảo vệ trung bình kèm khoảng tin cậy Bootstrap 95% ($p < 0.05$).

---

### Giả thuyết H2: Giá trị dự báo của chỉ số UGI
* **Mệnh đề:** Chỉ số UGI (Understood-Growth Index) dự báo kết quả thi bảo vệ cuối kỳ chính xác hơn đáng kể so với việc chỉ nhìn vào % tiến độ hoàn thành task.
* **Phương pháp đo:** Tính toán hệ số tương quan thứ hạng Spearman ($r_s$) và diện tích dưới đường cong ROC (AUC) giữa UGI với điểm thi thực tế.

---

### Giả thuyết H3: Hiệu quả của Vòng Lặp Dual-Dataset
* **Mệnh đề:** Cơ chế bổ trợ hai chiều giữa Gold Dataset và Generated Dataset giúp tăng chỉ số `hit@k` và `macro-F1` trong việc gợi ý câu hỏi phù hợp mà không gây suy giảm chất lượng dữ liệu mỏ neo.
* **Phương pháp đo:** Chạy thí nghiệm bóc tách (Ablation Study):
  1. Chỉ dùng Gold Dataset.
  2. Chỉ dùng LLM sinh tự do (Zero-shot).
  3. Kết hợp Dual-Dataset (Ánh xạ + Bổ trợ 2 chiều).

---

### Giả thuyết H4: Độ ổn định và Khả năng chịu tải của Hệ thống
* **Mệnh đề:** Hệ thống duy trì độ trễ phản hồi SSE dưới 800ms đối với token đầu tiên và tỷ lệ lỗi API dưới 0.1% khi chạy thử nghiệm tải giả lập 50 sinh viên cùng tương tác đồng thời.
* **Phương pháp đo:** Sử dụng công cụ Locust hoặc k6 để giả lập tải và xuất báo cáo biểu đồ thời gian thực.
