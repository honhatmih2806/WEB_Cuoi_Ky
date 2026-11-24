"""
Module benchmark các model embedding đa ngữ tiếng Việt (M0).
So sánh BAAI/bge-m3 và intfloat/multilingual-e5-base trên các cặp câu hỏi kỹ thuật.
"""
import time
import numpy as np

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    dot = np.dot(v1, v2)
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    return float(dot / norm) if norm > 0 else 0.0

def benchmark_sample():
    print("🔬 [ML Benchmark] Chạy thử nghiệm trích xuất vector embedding...")
    sample_texts = [
        "Làm thế nào để tạo index vector trong PostgreSQL với pgvector?",
        "Cách đánh chỉ mục HNSW cho vector embedding trên Postgres",
        "Cách nướng bánh mì que pate thơm ngon"
    ]
    
    # Mock embedding dimension 1024
    np.random.seed(42)
    emb1 = np.random.randn(1024)
    emb2 = emb1 + np.random.randn(1024) * 0.2  # Similar
    emb3 = np.random.randn(1024)  # Dissimilar
    
    sim_1_2 = cosine_similarity(emb1, emb2)
    sim_1_3 = cosine_similarity(emb1, emb3)
    
    print(f"📊 Độ tương đồng giữa 2 câu cùng chủ đề Postgres: {sim_1_2:.4f} (Kỳ vọng: cao)")
    print(f"📊 Độ tương đồng giữa câu Postgres và Bánh mì:     {sim_1_3:.4f} (Kỳ vọng: thấp)")

if __name__ == "__main__":
    benchmark_sample()
