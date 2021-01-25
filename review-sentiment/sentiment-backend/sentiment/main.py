from typing import Any, Dict, Optional

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from pydantic import BaseModel, validator

from .config import settings
from .explainer.explainer import EXPLAINERS, Explanation, explain
from .model.predict import Prediction, predict
from .routers import frontend
from .tracing import set_up_tracing

trace.set_tracer_provider(TracerProvider())
set_up_tracing(settings)

app = FastAPI()
app.include_router(frontend.router)


class PredictionRequest(BaseModel):
    text: str

    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Text must not be empty')
        return v


class ExplanationRequest(BaseModel):
    text: str
    target: int = settings.default_target
    method: str = settings.default_explainer
    settings: Optional[Dict[str, Any]]

    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Text must not be empty')
        return v

    @validator('target')
    def target_must_be_in_range(cls, v):
        if v < 0 or v > 4:
            raise ValueError('Target must be between 0 and 4')
        return v

    @validator('method')
    def method_must_be_available(cls, v):
        if v not in EXPLAINERS:
            raise ValueError(f'{v} is not an available explanation method')
        return v


@app.post('/predict')
async def predict_sentiment(request: PredictionRequest) -> Prediction:
    return predict(text=request.text)


@app.post('/explain')
async def explain_sentiment(request: ExplanationRequest) -> Explanation:
    return explain(text=request.text,
                   target=request.target,
                   explainer=request.method,
                   settings=request.settings)


FastAPIInstrumentor.instrument_app(app)
