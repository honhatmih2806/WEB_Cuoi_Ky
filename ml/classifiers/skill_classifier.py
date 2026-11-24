"""
Bộ phân loại Skill / Phase / Type từ prompt của sinh viên bằng Logistic Regression / SVM.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class SkillClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.model = LogisticRegression(max_iter=200)
        self.is_trained = False

    def train_baseline(self, texts: list[str], labels: list[str]):
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
        self.is_trained = True

    def predict(self, text: str) -> str:
        if not self.is_trained:
            # Baseline keyword fallback
            text_lower = text.lower()
            if "database" in text_lower or "sql" in text_lower or "vector" in text_lower:
                return "pgvector_sql"
            if "api" in text_lower or "fastapi" in text_lower or "endpoint" in text_lower:
                return "fastapi_rest"
            return "system_design"
        
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]
