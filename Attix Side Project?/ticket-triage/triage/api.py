import os
from contextlib import asynccontextmanager
from pathlib import Path
import joblib
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
from triage.model import normalize, predict

ROOT = Path(__file__).resolve().parents[1]

class Ticket(BaseModel):
    text: str = Field(min_length=3, max_length=5000)

    @field_validator("text")
    @classmethod
    def meaningful_text(cls, value):
        if len(normalize(value)) < 3 or not any(c.isalpha() for c in value):
            raise ValueError("Enter at least three characters including letters")
        return value

class Prediction(BaseModel):
    category: str
    score: float
    needs_review: bool
    reason: str
    scores: dict[str, float]
    model_version: str

@asynccontextmanager
async def lifespan(app):
    path = Path(os.getenv("MODEL_PATH", str(ROOT / "artifacts/model.joblib")))
    if not path.is_file():
        raise RuntimeError("Model missing. Run: python -m triage.train")
    # Only load artifacts built by this project. Pickle/joblib is not safe for untrusted files.
    app.state.bundle = joblib.load(path)
    yield

app = FastAPI(title="Support Ticket Triage", version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health(request: Request):
    return {"status": "ok", "model_version": request.app.state.bundle["version"]}

@app.post("/predict", response_model=Prediction)
def classify(ticket: Ticket, request: Request):
    bundle = request.app.state.bundle
    return {**predict(bundle["model"], ticket.text), "model_version": bundle["version"]}

@app.get("/", include_in_schema=False)
def demo():
    return FileResponse(ROOT / "static/index.html")
