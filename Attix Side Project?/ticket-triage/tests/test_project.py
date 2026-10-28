from pathlib import Path
import joblib
import pytest
from fastapi.testclient import TestClient
from triage.api import app
from triage.model import make_model, normalize, predict
from triage.train import ROOT, read_data

@pytest.fixture(scope="session")
def trained():
    x, y = read_data(ROOT / "data/train.csv")
    return make_model().fit(x, y)

@pytest.fixture()
def client(trained, tmp_path, monkeypatch):
    path = tmp_path / "model.joblib"
    joblib.dump({"model": trained, "version": "test-model"}, path)
    monkeypatch.setenv("MODEL_PATH", str(path))
    with TestClient(app) as c:
        yield c

def test_normalization():
    assert normalize("  CONTACT Me@Example.com\nhttps://example.com  ") == "contact emailtoken urltoken"

def test_split_is_disjoint():
    a, _ = read_data(ROOT / "data/train.csv")
    b, _ = read_data(ROOT / "data/test.csv")
    assert not set(map(normalize, a)) & set(map(normalize, b))

def test_vocabulary_learned_only_from_train(trained):
    assert "quasarzz" not in trained.named_steps["tfidf"].vocabulary_
    assert predict(trained, "quasarzz nebulaqq")["reason"] == "no_known_tokens"

def test_review_threshold(trained):
    assert predict(trained, "invoice payment", threshold=1.0)["needs_review"]

@pytest.mark.parametrize("text,label", [("I forgot my password", "account"), ("Please cancel my subscription", "cancellation"), ("My invoice was charged twice", "billing"), ("The app crashes on upload", "technical")])
def test_api_classification(client, text, label):
    r = client.post("/predict", json={"text": text})
    assert r.status_code == 200
    d = r.json()
    assert d["category"] == label
    assert sum(d["scores"].values()) == pytest.approx(1, abs=0.001)
    assert d["model_version"] == "test-model"

@pytest.mark.parametrize("text", ["", "   ", "12345", "x" * 5001])
def test_invalid_input(client, text):
    assert client.post("/predict", json={"text": text}).status_code == 422

def test_health_and_demo(client):
    assert client.get("/health").json()["status"] == "ok"
    assert "Support Ticket Triage" in client.get("/").text

def test_missing_model_fails_startup(monkeypatch, tmp_path):
    monkeypatch.setenv("MODEL_PATH", str(tmp_path / "missing.joblib"))
    with pytest.raises(RuntimeError, match="Model missing"):
        with TestClient(app):
            pass

def test_serialization_parity(trained, tmp_path):
    path = tmp_path / "model.joblib"
    joblib.dump(trained, path)
    assert predict(trained, "refund my payment") == predict(joblib.load(path), "refund my payment")
