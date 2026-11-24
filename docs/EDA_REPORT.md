# BÁO CÁO PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA REPORT)
> **Hệ thống:** ThinkBuild Defense-First Platform
> **Ngày thực hiện:** 22/11/2026
> **Mục tiêu:** Rà soát lỗi dữ liệu, khảo sát phân bố và đề xuất phương án làm sạch chuẩn hóa.

## 1. Phân Tích Dataset 1: Placement Interview Quiz (5.7K MCQs)
- **Tổng số bản ghi:** 5,699 câu hỏi
- **Số câu hỏi trùng lặp (Duplicates):** 229 câu (4.02%) ⚠️ *Cần lọc bỏ*
- **Độ dài câu hỏi (ký tự):** Ngắn nhất = 4, Dài nhất = 310, Trung bình = 42.0

### Phân bố theo chuyên mục (Section):
| Chuyên mục | Số lượng | Tỷ lệ | Phù hợp với Đề tài Web + AI |
| :--- | :---: | :---: | :---: |
| AI & ML | 900 | 15.8% | ✅ Cực kỳ phù hợp |
| DevOps Engineer | 900 | 15.8% | ✅ Cực kỳ phù hợp |
| SAP Engineer | 900 | 15.8% | ❌ Không thuộc phạm vi |
| React Engineer | 899 | 15.8% | ✅ Cực kỳ phù hợp |
| Numerical Ability | 700 | 12.3% | ❌ Không thuộc phạm vi |
| Logical Reasoning | 700 | 12.3% | ❌ Không thuộc phạm vi |
| Verbal Ability | 700 | 12.3% | ❌ Không thuộc phạm vi |

### Phân bố theo độ khó (Difficulty):
| Độ khó | Số lượng | Tỷ lệ |
| :--- | :---: | :---: |
| Medium | 2,453 | 43.0% |
| Hard | 2,100 | 36.8% |
| Easy | 1,146 | 20.1% |

---

## 2. Phân Tích Dataset 2: Imbue Code Comprehension (54K Items)
- **Tổng số bài toán code:** 54,000 câu
- **Dạng bài Cloze (Điền logic vào UNKNOWN):** 17,002 câu (31.5%)
- **Dạng bài Trace Output (Dự đoán kết quả in ra):** 36,998 câu (68.5%)
- **Độ dài đoạn code (ký tự):** Min = 75, Max = 1332, Trung bình = 317.3
- **Đánh giá chất lượng:** 100% dữ liệu có cấu trúc hợp lệ, không có JSON lỗi. Format code Python rõ ràng, sẵn sàng làm nguồn dữ liệu cho Tầng 2 (Sandbox Execution).

---

## 3. Phân Tích Dataset 3: StackPulse High Quality (~20K Items)
- **Tổng số ca hỏi đáp:** 20,205 bài
- **Điểm vote StackOverflow trung bình:** 13.8 điểm
- **Tỷ lệ chứa thẻ HTML thô (`<p>`, `&lt;`, `&gt;`):** 20,203 (100.0%) ⚠️ *Lỗi lớn nhất*
- **Tỷ lệ chứa khối code (`<pre><code>`):** 14,682 (72.7%)
- **Tỷ lệ ký tự thoát escape (`\"`, `\n`):** 19,699 (97.5%) ⚠️ *Gây vỡ format khi parse*

### Top 15 Tags công nghệ phổ biến nhất:
| Tag công nghệ | Số lượng | Mảng kỹ thuật |
| :--- | :---: | :--- |
| `python` | 2,202 | Backend / Python / API |
| `javascript` | 1,978 | Web / Frontend |
| `java` | 1,663 | Ngôn ngữ khác |
| `android` | 1,623 | Ngôn ngữ khác |
| `c#` | 1,152 | Ngôn ngữ khác |
| `c++` | 919 | Ngôn ngữ khác |
| `ios` | 877 | Ngôn ngữ khác |
| `html` | 674 | Web / Frontend |
| `node.js` | 642 | Ngôn ngữ khác |
| `swift` | 641 | Ngôn ngữ khác |
| `php` | 598 | Ngôn ngữ khác |
| `reactjs` | 569 | Web / Frontend |
| `css` | 557 | Web / Frontend |
| `r` | 551 | Ngôn ngữ khác |
| `angular` | 432 | Ngôn ngữ khác |

---

## 4. Tổng Kết Các Lỗi Nghiêm Trọng & Giải Pháp Xử Lý

1. **Lỗi 1: Nhiễu loạn HTML & Ký tự thoát Escape (Ảnh hưởng nặng nhất ở StackPulse):**
   * *Hiện tượng:* Người dùng nhìn thấy chuỗi ký tự lạ như: `"N": "0"
 }, "Mo": {"N": "1"...` do định dạng DynamoDB JSON bị bọc trong thẻ `<pre><code>` và bị escape liên tiếp 2 lần.
   * *Giải pháp:* Dùng Regex bóc tách nội dung trong `<pre><code>...</code></pre>`, giải mã `html.unescape()` và bọc vào chuẩn Markdown ````python
...
````. Toàn bộ thẻ `<p>`, `<br>` chuyển đổi thành dấu xuống dòng tiêu chuẩn.
2. **Lỗi 2: Trùng lặp dữ liệu (Deduplication ở Placement Quiz):**
   * *Hiện tượng:* Có 229 câu hỏi xuất hiện trùng lặp từ 2 đến 3 lần.
   * *Giải pháp:* Sử dụng bảng băm `set` để chỉ giữ lại duy nhất câu hỏi đầu tiên xuất hiện.
3. **Lỗi 3: Lệch phạm vi chủ đề (Out of scope):**
   * *Hiện tượng:* Placement Quiz chứa 3.000 câu SAP, IQ, Tiếng Anh; StackPulse chứa Java, C#, Android không liên quan đến Web + AI.
   * *Giải pháp:* Thiết lập bộ lọc chuyên đề: Chỉ trích lọc các record thuộc `React`, `Python`, `AI/ML`, `DevOps/Docker`, `Database/SQL`.

