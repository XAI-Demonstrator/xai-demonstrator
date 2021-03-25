from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel, validator

from .config import settings
from .explainer.explainer import EXPLAINERS, Explanation, explain
from .model.predict import Prediction, predict

api = APIRouter()


class PredictionRequest(BaseModel):
    text: str

    @validator("text")
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Text must not be empty")
        return v


@api.post("/predict")
def predict_sentiment(request: PredictionRequest) -> Prediction:
    return predict(text=request.text)

@api.post("/load")
def load_model():
    model = bert.model
    tokenizer = bert.tokenizer


class ExplanationRequest(BaseModel):
    text: str
    target: int = settings.default_target
    method: str = settings.default_explainer
    settings: Optional[Dict[str, Any]]

    @validator("text")
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Text must not be empty")
        return v

    @validator("target")
    def target_must_be_in_range(cls, v):
        if v < 0 or v > 4:
            raise ValueError("Target must be between 0 and 4")
        return v

    @validator("method")
    def method_must_be_available(cls, v):
        if v not in EXPLAINERS:
            raise ValueError(f"{v} is not an available explanation method")
        return v


@api.post("/explain")
def explain_sentiment(request: ExplanationRequest) -> Explanation:
    return explain(text=request.text,
                   target=request.target,
                   explainer=request.method,
                   settings=request.settings)
