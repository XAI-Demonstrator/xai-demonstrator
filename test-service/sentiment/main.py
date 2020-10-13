import random as rd
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

app = FastAPI()


class ExplanationRequest(BaseModel):
    text: str


class ExplanationResponse(BaseModel):
    prediction_id: uuid.UUID
    prediction: str
    explanation_id: uuid.UUID
    explanation: str


class PredictionRequest(BaseModel):
    text: str


class PredictionResponse(BaseModel):
    prediction_id: uuid.UUID
    prediction: str


def predict(message: str):
    return rd.choice(["positive", "negative"])


def explain(message: str) -> str:
    word_list = message.split()
    try:
        return rd.choice(word_list)
    except IndexError:
        return ""


@app.get("/")
def frontend():
    return FileResponse("./static/frontend.html")


@app.post('/predict')
async def predict_sentiment(request: PredictionRequest):
    return PredictionResponse(prediction_id=uuid.uuid4(),
                              prediction=predict(request.text))


@app.post('/explain')
async def explain_sentiment(request: ExplanationRequest):
    return ExplanationResponse(
        prediction_id=uuid.uuid4(),
        prediction=predict(request.text),
        explanation_id=uuid.uuid4(),
        explanation=explain(request.text)
    )
