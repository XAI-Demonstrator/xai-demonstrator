import random as rd

from fastapi import FastAPI

app = FastAPI()


def predict(message: str):
    return rd.choice(["positive", "negative"])


def explain(message: str):
    word_list = message.split()
    return rd.choice(word_list)


@app.get("/")
async def read_root():
    return "Welcome to my service!"


@app.post('/predict', status_code=201)
async def predict_sentiment(payload: str):
    return {'prediction': predict(payload)}


@app.post('/explain', status_code=201)
async def explain_sentiment(payload: str):
    return {'prediction': predict(payload),
            'explanation': explain(payload)}
