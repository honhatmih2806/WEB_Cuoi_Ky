#!/usr/bin/env python3
"""
Pipeline tiền xử lý và chuẩn hóa dữ liệu cho ThinkBuild (M2).
Đọc dữ liệu thô từ data/raw/ và chuyển đổi sang data/processed/ theo schema chuẩn.
"""
import os
import csv
import json
import uuid

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)

def preprocess_placement_quiz():
    csv_file = os.path.join(RAW_DIR, "placement_interview_quiz", "Placement_Interview_Quiz_Questions.csv")
    output_file = os.path.join(PROCESSED_DIR, "knowledge_mcq.jsonl")

    if not os.path.exists(csv_file):
        print(f"⚠️ Không tìm thấy file {csv_file}")
        return

    print("⏳ [1/3] Đang xử lý Placement Interview Quiz (5.7K MCQs)...")
    target_sections = {"React Engineer", "AI & ML", "DevOps Engineer"}
    
    section_to_skill = {
        "React Engineer": "react_frontend",
        "AI & ML": "machine_learning",
        "DevOps Engineer": "devops_docker_ci"
    }

    count = 0
    with open(csv_file, mode="r", encoding="utf-8") as f_in, open(output_file, mode="w", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        for row in reader:
            section = row.get("section", "").strip()
            if section in target_sections:
                choices = [
                    f"A. {row.get('A', '').strip()}",
                    f"B. {row.get('B', '').strip()}",
                    f"C. {row.get('C', '').strip()}",
                    f"D. {row.get('D', '').strip()}",
                ]
                ans_letter = row.get("answer", "").strip().upper()
                
                # Map answer letter to choice text
                ref_ans = row.get(ans_letter, "").strip() if ans_letter in ["A", "B", "C", "D"] else ans_letter

                item = {
                    "id": str(uuid.uuid4()),
                    "original_id": row.get("id"),
                    "skill": section_to_skill.get(section, "general_cs"),
                    "phase_level": 1 if section == "React Engineer" else 3 if section == "AI & ML" else 5,
                    "type": "knowledge",
                    "question": row.get("question", "").strip(),
                    "choices": choices,
                    "reference_answer": ref_ans,
                    "difficulty": row.get("difficulty", "Medium").upper(),
                    "tags": [section.lower().replace(" ", "_"), row.get("topic", "").strip().lower()],
                    "source": "prepmaster_kaggle",
                    "license": "MIT",
                    "language": "en"
                }
                f_out.write(json.dumps(item, ensure_ascii=False) + "\n")
                count += 1

    print(f"✅ Đã chuẩn hóa {count} câu hỏi trắc nghiệm (React, AI/ML, DevOps) -> {output_file}")

def preprocess_imbue_code():
    input_file = os.path.join(RAW_DIR, "imbue_code_comprehension", "codegen.jsonl")
    output_file = os.path.join(PROCESSED_DIR, "code_comprehension.jsonl")

    if not os.path.exists(input_file):
        print(f"⚠️ Không tìm thấy file {input_file}")
        return

    print("⏳ [2/3] Đang xử lý Imbue Code Comprehension (54K items)...")
    count = 0
    max_items = 1000  # Trích lọc 1000 bài tập tiêu biểu
    with open(input_file, mode="r", encoding="utf-8") as f_in, open(output_file, mode="w", encoding="utf-8") as f_out:
        for line in f_in:
            if not line.strip():
                continue
            data = json.loads(line)
            item = {
                "id": str(uuid.uuid4()),
                "skill": "python_logic_tracing",
                "phase_level": 2,
                "type": "code_comprehension",
                "question": data.get("question", "").strip(),
                "choices": data.get("choices"),
                "reference_answer": str(data.get("correct_answer", "")).strip(),
                "difficulty": "MEDIUM",
                "tags": ["python", "execution_trace", "logic"],
                "source": "imbue_ai",
                "license": "MIT",
                "language": "en"
            }
            f_out.write(json.dumps(item, ensure_ascii=False) + "\n")
            count += 1
            if count >= max_items:
                break

    print(f"✅ Đã trích lọc {count} bài toán thấu hiểu code (Execution Tracing) -> {output_file}")

def preprocess_stackoverflow_sample():
    input_file = os.path.join(RAW_DIR, "stackpulse_stackoverflow", "stackoverflow_high_quality.jsonl")
    output_file = os.path.join(PROCESSED_DIR, "tech_troubleshooting.jsonl")

    if not os.path.exists(input_file):
        print(f"⚠️ Không tìm thấy file {input_file}")
        return

    print("⏳ [3/3] Đang xử lý StackPulse High Quality (~60MB)...")
    count = 0
    max_items = 500
    with open(input_file, mode="r", encoding="utf-8") as f_in, open(output_file, mode="w", encoding="utf-8") as f_out:
        for line in f_in:
            if not line.strip():
                continue
            data = json.loads(line)
            title = data.get("title", "")
            tags = data.get("tags", [])
            
            # Ưu tiên các câu hỏi về Web, Python, API, DB
            tags_str = " ".join(tags) if isinstance(tags, list) else str(tags)
            if any(k in tags_str for k in ["python", "javascript", "react", "fastapi", "sql", "docker", "api"]):
                item = {
                    "id": str(uuid.uuid4()),
                    "original_id": data.get("id"),
                    "title": title,
                    "question_body": data.get("body_text", "")[:1000],
                    "tags": tags if isinstance(tags, list) else [tags_str],
                    "score": data.get("score", 0),
                    "source": "stackpulse_stackoverflow",
                    "license": "Apache-2.0"
                }
                f_out.write(json.dumps(item, ensure_ascii=False) + "\n")
                count += 1
                if count >= max_items:
                    break

    print(f"✅ Đã trích lọc {count} ca xử lý lỗi kỹ thuật (Troubleshooting) -> {output_file}")

if __name__ == "__main__":
    preprocess_placement_quiz()
    preprocess_imbue_code()
    preprocess_stackoverflow_sample()
    print("🎉 Hoàn tất tiền xử lý toàn bộ dữ liệu!")
