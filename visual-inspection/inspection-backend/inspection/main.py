from typing import Dict
from fastapi import FastAPI, UploadFile, Form, File

from .routers import frontend
from .model.predict import predict, Prediction

app = FastAPI()
app.include_router(frontend.router)


@app.post("/predict")
def predict_weather(file: UploadFile = File(...)) -> Prediction:
    return predict(file.file)


@app.post("/explain")
def explain(file: UploadFile = File(...),
            method: str = "lime",
            settings: Dict = None):
    return file.filename
