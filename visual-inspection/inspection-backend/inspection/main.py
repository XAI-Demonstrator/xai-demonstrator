from typing import Any, Dict, Union

from fastapi import FastAPI, File, Form, UploadFile
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from pydantic import BaseModel, StrictFloat, StrictInt, validator

from .config import settings
from .explainer.explain import EXPLAINERS, Explanation, explain
from .model.predict import Prediction, predict
from .routers import frontend
from .tracing import set_up_tracing

trace.set_tracer_provider(TracerProvider())
set_up_tracing(settings)


class ExplanationRequest(BaseModel):
    method: str = settings.default_explainer
    settings: Dict[str, Union[StrictInt, StrictFloat, int, float, str]]

    @validator('method')
    def method_must_be_available(cls, v):
        if v not in EXPLAINERS:
            raise ValueError(f'{v} is not an available explanation method')
        return v


app = FastAPI()
app.include_router(frontend.router)


@app.post("/predict")
def predict_weather(file: UploadFile = File(...)) -> Prediction:
    return predict(file.file)


@app.post("/explain")
def explain_classification(file: UploadFile = File(...),
                           method: str = Form(settings.default_explainer),
                           exp_settings: Dict[str, Any] = Form({})) -> Explanation:
    request = ExplanationRequest(method=method,
                                 settings=exp_settings)

    return explain(file.file, method=request.method, settings=request.settings)


FastAPIInstrumentor.instrument_app(app)
