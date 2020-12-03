import random as rd
from typing import List
import uuid
import pathlib

from fastapi import FastAPI
from pydantic import BaseModel, validator
from fastapi.responses import FileResponse

from .model import model
from .explainer import gradient_explainer

import logging

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


class ExplanationResponse(BaseModel):
    prediction: model.Prediction
    explanation: gradient_explainer.Explanation


@app.get("/")
def frontend():
    return FileResponse(pathlib.Path(__file__).parent / "static/frontend.html")


@app.get("/charty.css")
def style():
    return FileResponse(pathlib.Path(__file__).parent / "static/charty.css")


@app.post('/predict')
async def predict_sentiment(request: PredictionRequest):
    return model.predict_sentiment(request.text)


@app.post('/explain')
async def explain_sentiment(request: ExplanationRequest) -> ExplanationResponse:
    # TODO: Parallelize
    prediction = model.predict_sentiment(request.text)
    # TODO: Allow explanation based on prediction
    explanation = gradient_explainer.explain(request.text, request.target)
    return ExplanationResponse(prediction=prediction, explanation=explanation)
