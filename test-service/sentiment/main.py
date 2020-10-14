import random as rd
from typing import List
import uuid
import pathlib

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

from .model import model

import logging

app = FastAPI()

logger = logging.getLogger("api")


class ExplanationRequest(BaseModel):
    text: str


class ExplanationResponse(BaseModel):
    prediction_id: uuid.UUID
    prediction: List[float]
    explanation_id: uuid.UUID
    explanation: str


class PredictionRequest(BaseModel):
    text: str


class PredictionResponse(BaseModel):
    prediction_id: uuid.UUID
    prediction: List[float]


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
    return PredictionResponse(prediction_id=uuid.uuid4(),
                              prediction=model.predict_sentiment(request.text))


@app.post('/explain')
async def explain_sentiment(request: ExplanationRequest):
    return ExplanationResponse(
        prediction_id=uuid.uuid4(),
        prediction=model.predict_sentiment(request.text),
        explanation_id=uuid.uuid4(),
        explanation=explain(request.text)
    )
