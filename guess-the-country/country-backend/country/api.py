from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from .streetview.client import get_random_streetview_image, StreetViewImage
from .model.predict import predict_city, Prediction
from .explainer.explain import explain, Explanation
from pydantic import BaseModel
from .config import settings

api = APIRouter()


class ScoreRequest(BaseModel):
    # gameStore
    round: int
    roundOffset: int
    totalNumOfRounds: int
    aiScore: int
    humanScore: int
    gameId: str
    playerId: str
    # roundStore
    trueCity: str
    trueCountry: str
    aiCity: str
    aiCountry: str
    humanCity: str
    humanCountry: str
    currentRound: int
    predictionId: str
    explanationId: str


class FinalScoreResponse(BaseModel):
    totalNumOfRounds: int = 0
    scoreAi: int = 0
    scoreHuman: int = 0


@api.post("/streetview")
async def streetview(score_request: ScoreRequest) -> StreetViewImage:
    if not settings.streetview_static_api_token:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="No StreetView API key was provided to the backend service!")
    return await get_random_streetview_image()


@api.post("/predict")
def predict(file: UploadFile = File(...)) -> Prediction:
    return predict_city(file.file)


# Explain Prediction
@api.post("/explain")
async def explain_api(file: UploadFile = File(...)) -> Explanation:
    return explain(file.file)


@api.post("/score")
async def score(score_request: ScoreRequest):
    pass


@api.get("/final_score")
def final_score() -> FinalScoreResponse:
    return FinalScoreResponse()
