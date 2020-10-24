import random as rd
from typing import List
import uuid
import pathlib

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

from .model import model
from .explainer import gradient_explainer

import logging

app = FastAPI()

logger = logging.getLogger("api")


class PredictionRequest(BaseModel):
    text: str


class ExplanationRequest(BaseModel):
    text: str


class ExplanationResponse(BaseModel):
    prediction: model.Prediction
    explanation: gradient_explainer.Explanation


def explain(message: str) -> str:
    word_list = message.split()
    try:
        return rd.choice(word_list)
    except IndexError:
        return ""


@app.get("/")
def frontend():
    return FileResponse(pathlib.Path(__file__).parent/"static/frontend.html")


@app.post('/predict')
async def predict_sentiment(request: PredictionRequest):
    return model.predict_sentiment(request.text)


@app.post('/explain')
async def explain_sentiment(request: ExplanationRequest) -> ExplanationResponse:
    prediction, explanation = gradient_explainer.explain(request.text)
    return ExplanationResponse(prediction=prediction, explanation=explanation)
