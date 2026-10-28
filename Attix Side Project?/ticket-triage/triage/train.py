"""Train only on train.csv; evaluate once on the separately authored test.csv."""
import csv
import hashlib
import json
from pathlib import Path
import joblib
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from triage.model import LABELS, THRESHOLD, make_model, normalize, predict

ROOT = Path(__file__).resolve().parents[1]

def read_data(path):
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows or any(r["label"] not in LABELS or not normalize(r["text"]) for r in rows):
        raise ValueError(f"Invalid dataset: {path}")
    normalized = [normalize(r["text"]) for r in rows]
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"Duplicate input in {path}")
    if set(r["label"] for r in rows) != set(LABELS):
        raise ValueError("Every dataset must contain every category")
    return [r["text"] for r in rows], [r["label"] for r in rows]

def train(root=ROOT):
    x_train, y_train = read_data(root / "data/train.csv")
    x_test, y_test = read_data(root / "data/test.csv")
    if set(map(normalize, x_train)) & set(map(normalize, x_test)):
        raise ValueError("Train/test overlap detected")
    model = make_model().fit(x_train, y_train)
    predictions = model.predict(x_test)
    baseline = DummyClassifier(strategy="most_frequent").fit(x_train, y_train).predict(x_test)
    decisions = [predict(model, text) for text in x_test]
    accepted = [i for i, d in enumerate(decisions) if not d["needs_review"]]
    data_hash = hashlib.sha256((root / "data/train.csv").read_bytes()).hexdigest()
    version = "tfidf-logreg-v1-" + data_hash[:12]
    report = {
        "model_version": version, "sklearn_version": sklearn.__version__,
        "data_type": "synthetic demonstration; not real-world performance",
        "train_count": len(x_train), "test_count": len(x_test),
        "train_sha256": data_hash,
        "test_sha256": hashlib.sha256((root / "data/test.csv").read_bytes()).hexdigest(),
        "accuracy": accuracy_score(y_test, predictions),
        "macro_f1": f1_score(y_test, predictions, average="macro"),
        "baseline_accuracy": accuracy_score(y_test, baseline),
        "baseline_macro_f1": f1_score(y_test, baseline, average="macro"),
        "threshold": THRESHOLD, "automation_coverage": len(accepted)/len(x_test),
        "accepted_accuracy": sum(predictions[i] == y_test[i] for i in accepted)/len(accepted) if accepted else None,
        "labels": LABELS,
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=LABELS).tolist(),
        "per_class": classification_report(y_test, predictions, output_dict=True, zero_division=0),
        "errors": [{"text": x_test[i], "expected": y_test[i], "predicted": str(predictions[i])}
                   for i in range(len(x_test)) if y_test[i] != predictions[i]],
    }
    (root / "artifacts").mkdir(exist_ok=True)
    (root / "reports").mkdir(exist_ok=True)
    joblib.dump({"model": model, "version": version}, root / "artifacts/model.joblib")
    (root / "reports/evaluation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    train()
