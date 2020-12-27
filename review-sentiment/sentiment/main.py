import logging
import pathlib

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, validator

from .explainer.explainer import Explanation, explain, EXPLAINERS
from .model.predict import Prediction, predict

app = FastAPI()

logger = logging.getLogger("api")


class PredictionRequest(BaseModel):
    text: str

    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Text must not be empty')
        return v


class ExplanationRequest(BaseModel):
    text: str
    target: int = 4
    method: str = "integrated_gradients"

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


class ExplanationResponse(BaseModel):
    prediction: Prediction
    explanation: Explanation


@app.get("/")
def frontend():
    return FileResponse(pathlib.Path(__file__).parent / "static" / "index.html")


@app.get("/favicon.ico")
def favicon():
    return FileResponse(pathlib.Path(__file__).parent / "static" / "favicon.ico")


@app.get("/css/{fname}")
def style(fname):
    return FileResponse(pathlib.Path(__file__).parent / "static" / "css" / fname)


@app.get("/js/{fname}")
def script(fname):
    return FileResponse(pathlib.Path(__file__).parent / "static" / "js" / fname)


@app.get("/img/{fname}")
def script(fname):
    return FileResponse(pathlib.Path(__file__).parent / "static" / "img" / fname)


@app.post('/predict')
async def predict_sentiment(request: PredictionRequest):
    return predict(request.text)


@app.post('/explain')
async def explain_sentiment(request: ExplanationRequest) -> ExplanationResponse:
    # TODO: Parallelize
    prediction = predict(request.text)
    # TODO: Allow explanation based on prediction
    explanation = explain(request.text, request.target, request.method)
    return ExplanationResponse(prediction=prediction, explanation=explanation)
