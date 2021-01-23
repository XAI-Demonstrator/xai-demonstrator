import base64
import io

from fastapi import FastAPI, File, UploadFile

from .explainer.explain import explain
from .model.predict import Prediction, predict
from .routers import frontend

app = FastAPI()
app.include_router(frontend.router)


@app.post("/predict")
def predict_weather(file: UploadFile = File(...)) -> Prediction:
    return predict(file.file)


# TODO: Define explanation request input and response content
@app.post("/explain")
def get_explanation(file: UploadFile = File(...)):
    exp_image = explain(file.file)

    buffered = io.BytesIO()
    exp_image.save(buffered, format="png")

    encoded_image_string = base64.b64encode(buffered.getvalue())
    return {"image": bytes("data:image/png;base64,", encoding='utf-8') + encoded_image_string}
