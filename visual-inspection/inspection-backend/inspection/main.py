from typing import Dict
import base64
from PIL import Image
import io

from fastapi import FastAPI, File, UploadFile

from .model.predict import Prediction, predict
from .routers import frontend

app = FastAPI()
app.include_router(frontend.router)


@app.post("/predict")
def predict_weather(file: UploadFile = File(...)) -> Prediction:
    return predict(file.file)


@app.post("/explain")
def explain(file: UploadFile = File(...)):
    img = Image.open(file.file)
    rotated = img.rotate(180)

    buffered = io.BytesIO()
    rotated.save(buffered, format="png")

    encoded_image_string = base64.b64encode(buffered.getvalue())
    return {"image": bytes("data:image/png;base64,", encoding='utf-8') + encoded_image_string}
