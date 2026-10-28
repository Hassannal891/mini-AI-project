import re
import unicodedata
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

LABELS = ["account", "billing", "cancellation", "technical"]
THRESHOLD = 0.55  # Illustrative policy, not tuned on the test set.

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"https?://\S+", " urltoken ", text)
    text = re.sub(r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b", " emailtoken ", text)
    return " ".join(text.split())

def make_model():
    return Pipeline([
        ("tfidf", TfidfVectorizer(preprocessor=normalize, ngram_range=(1, 2), sublinear_tf=True)),
        ("classifier", LogisticRegression(C=4.0, max_iter=1000, random_state=42)),
    ])

def predict(model, text: str, threshold: float = THRESHOLD):
    probabilities = model.predict_proba([text])[0]
    scores = dict(zip(model.classes_, map(float, probabilities)))
    label = max(scores, key=scores.get)
    known_tokens = model.named_steps["tfidf"].transform([text]).nnz > 0
    review = not known_tokens or scores[label] < threshold
    return {
        "category": label,
        "score": round(scores[label], 4),
        "needs_review": review,
        "reason": "no_known_tokens" if not known_tokens else ("low_score" if review else "above_threshold"),
        "scores": {k: round(v, 4) for k, v in scores.items()},
    }
