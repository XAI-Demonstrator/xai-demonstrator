from fastapi import FastAPI
from pydantic import BaseModel

from .model.predict import predict, Prediction
from .routers import frontend

app = FastAPI()
app.include_router(frontend.router)


# TODO: Define image payload etc.
class PredictionRequest(BaseModel):
    image: str


@app.post('/predict')
async def predict_weather(request: PredictionRequest) -> Prediction:
    return predict(request.image)
