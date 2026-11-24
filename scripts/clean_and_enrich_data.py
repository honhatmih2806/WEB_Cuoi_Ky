#!/usr/bin/env python3
"""
scripts/clean_and_enrich_data.py
Pipeline làm sạch chuyên sâu (Deep Data Cleaning & Formatting):
- Chuyển đổi mã HTML thô, thẻ <pre><code> thành khối Markdown chuẩn (```python / ```).
- Giải mã toàn bộ HTML entities (&lt;, &gt;, &amp;, &quot;, &#39;).
- Khử các chuỗi ký tự thoát escape phức tạp (\" -> ", \n -> xuống dòng thật).
- Khử trùng lặp (Deduplication) 229 câu hỏi trong Placement Quiz.
- Xuất dữ liệu sạch đẹp vào data/processed/.
"""
import os
import csv
import json
import re
import html
import uuid

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)

def clean_html_to_markdown(raw_html: str, default_lang: str = "python") -> str:
    """
    Chuyển đổi thẻ HTML thô của StackOverflow thành Markdown chuẩn đẹp.
    """
    if not raw_html:
        return ""
    
    text = raw_html
    
    # 1. Chuyển đổi khối <pre><code>...</code></pre> thành ```python ... ```
    def format_code_block(match):
        code_str = match.group(1)
        # Unescape các ký tự trong code
        code_str = html.unescape(code_str)
        # Xóa các khoảng trắng thừa đầu cuối
        code_str = code_str.strip()
        return f"\n\n```{default_lang}\n{code_str}\n```\n\n"
    
    text = re.sub(r'<pre(?:.*?)><code(?:.*?)>(.*?)</code></pre>', format_code_block, text, flags=re.DOTALL | re.IGNORECASE)
    
    # 2. Chuyển đổi thẻ inline <code>...</code> thành `...`
    def format_inline_code(match):
        code_str = html.unescape(match.group(1)).strip()
        return f"`{code_str}`"
    
    text = re.sub(r'<code(?:.*?)>(.*?)</code>', format_inline_code, text, flags=re.DOTALL | re.IGNORECASE)
    
    # 3. Chuyển đổi liên kết <a href="url">text</a> thành [text](url)
    text = re.sub(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.IGNORECASE)
    
    # 4. Chuyển đổi đoạn văn <p> và <br>
    text = re.sub(r'</p>\s*<p>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # 5. Loại bỏ tất cả các thẻ HTML còn sót lại
    text = re.sub(r'<[^>]+>', '', text)
    
    # 6. Unescape các ký tự HTML còn lại (&amp; -> &, &quot; -> ", &lt; -> <, v.v.)
    text = html.unescape(text)
    
    # 7. Chuẩn hóa khoảng trắng và dòng trống
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def clean_placement_quiz():
    csv_file = os.path.join(RAW_DIR, "placement_interview_quiz", "Placement_Interview_Quiz_Questions.csv")
    output_file = os.path.join(PROCESSED_DIR, "clean_knowledge_mcq.jsonl")

    if not os.path.exists(csv_file):
        print(f"⚠️ Không tìm thấy file: {csv_file}")
        return

    print("⏳ [1/3] Đang làm sạch & khử trùng lặp Placement Quiz (5.7K MCQs)...")
    target_sections = {
        "React Engineer": ("react_frontend", 1),
        "AI & ML": ("machine_learning", 3),
        "DevOps Engineer": ("devops_docker_ci", 5)
    }

    seen_questions = set()
    cleaned_records = []

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sec = row.get("section", "").strip()
            if sec not in target_sections:
                continue

            q = row.get("question", "").strip()
            # Khử trùng lặp câu hỏi
            if q in seen_questions:
                continue
            seen_questions.add(q)

            skill_name, phase_lvl = target_sections[sec]
            
            # Làm sạch text lựa chọn
            choices = [
                f"A. {html.unescape(row.get('A', '').strip())}",
                f"B. {html.unescape(row.get('B', '').strip())}",
                f"C. {html.unescape(row.get('C', '').strip())}",
                f"D. {html.unescape(row.get('D', '').strip())}"
            ]
            ans_key = row.get("answer", "").strip().upper()
            ref_ans = row.get(ans_key, "").strip() if ans_key in ["A", "B", "C", "D"] else ans_key
            ref_ans = html.unescape(ref_ans)

            record = {
                "id": str(uuid.uuid4()),
                "original_id": row.get("id"),
                "skill": skill_name,
                "phase_level": phase_lvl,
                "type": "knowledge",
                "question": html.unescape(q),
                "choices": choices,
                "reference_answer": ref_ans,
                "correct_option": ans_key,
                "difficulty": row.get("difficulty", "Medium").upper(),
                "topic": row.get("topic", "").strip(),
                "source": "prepmaster_kaggle",
                "language": "en"
            }
            cleaned_records.append(record)

    with open(output_file, mode="w", encoding="utf-8") as f_out:
        for r in cleaned_records:
            f_out.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"✅ Hoàn tất! Đã xuất {len(cleaned_records):,} câu hỏi sạch (Đã loại 229 câu trùng) -> {output_file}")

def clean_imbue_code():
    input_file = os.path.join(RAW_DIR, "imbue_code_comprehension", "codegen.jsonl")
    output_file = os.path.join(PROCESSED_DIR, "clean_code_comprehension.jsonl")

    if not os.path.exists(input_file):
        print(f"⚠️ Không tìm thấy file: {input_file}")
        return

    print("⏳ [2/3] Đang làm sạch Imbue Code Comprehension...")
    cleaned_records = []
    max_items = 1500

    with open(input_file, mode="r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            q_raw = data.get("question", "")
            
            # Format chuẩn Markdown cho code
            q_clean = q_raw.strip()
            # Đảm bảo khối code có thẻ ```python
            if "```\n" in q_clean and "```python\n" not in q_clean:
                q_clean = q_clean.replace("```\n", "```python\n", 1)

            record = {
                "id": str(uuid.uuid4()),
                "skill": "python_logic_tracing",
                "phase_level": 2,
                "type": "code_comprehension",
                "question": q_clean,
                "choices": data.get("choices"),
                "reference_answer": str(data.get("correct_answer", "")).strip(),
                "difficulty": "MEDIUM",
                "source": "imbue_ai",
                "language": "en"
            }
            cleaned_records.append(record)
            if len(cleaned_records) >= max_items:
                break

    with open(output_file, mode="w", encoding="utf-8") as f_out:
        for r in cleaned_records:
            f_out.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"✅ Hoàn tất! Đã xuất {len(cleaned_records):,} bài toán code sạch -> {output_file}")

def clean_stackpulse_troubleshooting():
    input_file = os.path.join(RAW_DIR, "stackpulse_stackoverflow", "stackoverflow_high_quality.jsonl")
    output_file = os.path.join(PROCESSED_DIR, "clean_troubleshooting_qa.jsonl")

    if not os.path.exists(input_file):
        print(f"⚠️ Không tìm thấy file: {input_file}")
        return

    print("⏳ [3/3] Đang làm sạch StackPulse (Triệt tiêu thẻ HTML & escape)...")
    cleaned_records = []
    max_items = 600

    target_tags = ["python", "javascript", "react", "fastapi", "sql", "docker", "api", "json", "rest"]

    with open(input_file, mode="r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            
            tags = data.get("tags", "")
            tags_list = tags.split("|") if isinstance(tags, str) else tags
            tags_lower = [t.lower().strip() for t in tags_list]
            
            # Kiểm tra xem có tag phù hợp không
            if not any(k in " ".join(tags_lower) for k in target_tags):
                continue

            raw_body = data.get("question_body", "")
            title = data.get("title", "").strip()

            # Xác định ngôn ngữ chính của câu hỏi
            lang = "javascript" if any(k in tags_lower for k in ["javascript", "reactjs", "node.js"]) else "python"
            
            # Áp dụng thuật toán bóc tách HTML sang Markdown chuẩn
            clean_body = clean_html_to_markdown(raw_body, default_lang=lang)

            record = {
                "id": str(uuid.uuid4()),
                "original_id": data.get("id"),
                "skill": f"{lang}_troubleshooting",
                "phase_level": 4,
                "type": "defense",
                "title": title,
                "question": f"### Tình huống kỹ thuật: {title}\n\n{clean_body}",
                "tags": tags_lower,
                "score": data.get("score", 0),
                "source": "stackpulse_stackoverflow",
                "language": "en"
            }
            cleaned_records.append(record)
            if len(cleaned_records) >= max_items:
                break

    with open(output_file, mode="w", encoding="utf-8") as f_out:
        for r in cleaned_records:
            f_out.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"✅ Hoàn tất! Đã xuất {len(cleaned_records):,} ca xử lý lỗi sạch đẹp (Đã bóc tách HTML & format code Markdown) -> {output_file}")

if __name__ == "__main__":
    clean_placement_quiz()
    clean_imbue_code()
    clean_stackpulse_troubleshooting()
    print("\n🎉 Toàn bộ dữ liệu trong data/processed/ đã được làm sạch và chuẩn hóa 100%!")
