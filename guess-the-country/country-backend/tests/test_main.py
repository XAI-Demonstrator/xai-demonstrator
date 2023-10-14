import pytest
from httpx import AsyncClient
import uuid
from fastapi.testclient import TestClient
from country import main
from country.api import ScoreRequest


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=main.app, base_url="http://test") as async_client:
        print("Client is ready")
        yield async_client


client = TestClient(main.app)


@pytest.fixture
def random_score_request():
    return ScoreRequest(
        round=1,
        roundOffset=0,
        totalNumOfRounds=2,
        aiScore=1,
        humanScore=0,
        gameId=str(uuid.uuid4()),
        playerId=str(uuid.uuid4()),
        trueCity="Ulm",
        trueCountry="Germany",
        aiCity="Ulm",
        aiCountry="Germany",
        humanCity="Hamburg",
        humanCountry="Germany",
        currentRound=1,
        predictionId=str(uuid.uuid4()),
        explanationId=str(uuid.uuid4()),
    )


@pytest.mark.streetview
@pytest.mark.anyio
async def test_that_requesting_a_streetview_image_succeeds(
    random_score_request, async_client
):
    response = await async_client.post(
        "http://test/streetview", json=random_score_request.dict()
    )

    assert response.status_code == 200


@pytest.mark.integration
def test_that_prediction_succeeds(generate_png_image):
    response = client.post("/predict", files={"file": generate_png_image(448, 448)})

    assert response.status_code == 200


@pytest.mark.integration
def test_that_explanation_succeeds(generate_png_image):
    response = client.post("/explain", files={"file": generate_png_image(448, 448)})

    assert response.status_code == 200
