import os
import sys
import json

# Add apps/api to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "api")))

from core.database import SessionLocal
from models.entities import GoldItem

def ingest_gold_data():
    seed_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "gold", "seed_gold_web_ai.json"))
    if not os.path.exists(seed_file):
        print(f"❌ Không tìm thấy file {seed_file}")
        return

    print(f"⏳ [ingest_gold] Đang đọc file dữ liệu: {seed_file}...")
    with open(seed_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    db = SessionLocal()
    try:
        count = 0
        for item in data:
            existing = db.query(GoldItem).filter(GoldItem.question == item["question"]).first()
            if not existing:
                gold_record = GoldItem(
                    skill=item["skill"],
                    phase_level=item["phase_level"],
                    type=item["type"],
                    question=item["question"],
                    choices=item.get("choices"),
                    reference_answer=item["reference_answer"],
                    rubric=item.get("rubric"),
                    explanation=item.get("explanation"),
                    difficulty=item.get("difficulty", "MEDIUM"),
                    tags=item.get("tags", []),
                    source=item.get("source", "thinkbuild_gold"),
                    license=item.get("license", "MIT"),
                    language=item.get("language", "vi")
                )
                db.add(gold_record)
                count += 1
        db.commit()
        print(f"✅ Đã nạp thành công {count} câu hỏi mẫu vào Gold Dataset!")
    finally:
        db.close()

if __name__ == "__main__":
    ingest_gold_data()
