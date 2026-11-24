"""
Vector Search & Reranking Engine giữa Generated Items và Gold Items.
Xác định quan hệ: reinforce, conflict, extend, new.
"""
import numpy as np

def compute_relation(similarity: float, judge_agreement: bool) -> str:
    """
    Quy tắc 4 trạng thái Dual-Dataset:
    - reinforce: similarity cao (> 0.85) và judge đồng thuận.
    - conflict: similarity cao (> 0.85) nhưng nội dung/đáp án mâu thuẫn -> vào review_queue.
    - extend: similarity trung bình (0.65 - 0.85) -> mở rộng ví dụ thực tế.
    - new: similarity thấp (< 0.65) -> vùng cách ly đánh giá.
    """
    if similarity >= 0.85:
        return "reinforce" if judge_agreement else "conflict"
    elif similarity >= 0.65:
        return "extend"
    else:
        return "new"
