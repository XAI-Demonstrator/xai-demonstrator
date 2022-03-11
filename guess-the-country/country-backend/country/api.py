from fastapi import APIRouter, UploadFile, File
from .config import settings
from .streetview.collect import get_streetview
from .model.predict import prediction
from .explainer.explain import explain


api = APIRouter()

# Google Street View Image API
# 25,000 image requests per 24 hours
# See https://developers.google.com/maps/documentation/streetview/
API_KEY = settings.google_maps_api_token

@api.post("/predict")
def predict(file: UploadFile = File(...)):
    return prediction(file.file.read())


# Explain Prediction
@api.post("/explain")
async def explain_api(file: UploadFile = File(...)):
    return explain(file.file.read())


@api.get("/msg")
def home():
    return {
        "data": "Your guess: Where has this Google Streetview picture been taken?"
    }

@api.post("/score")
async def score():
    return {}

@api.get("/streetview")
async def streetview():
    return await get_streetview(API_KEY)


