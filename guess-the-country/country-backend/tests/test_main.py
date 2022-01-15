import pytest
from fastapi.testclient import TestClient

from country import main

client = TestClient(main.app)


@pytest.mark.integration
def test_that_prediction_succeeds(generate_image):
    response = client.post("/predict", files={"file": generate_image(448, 448)})

    assert response.status_code == 200


@pytest.mark.integration
def test_that_explanation_succeeds(generate_image):
    r = client.post("/explain", files={"file": generate_image(448, 448)})

    assert r.status_code == 200

@pytest.mark.integration
def test_that_msg_succeeds(generate_image):
    r = client.post("/msg")

    assert r.status_code == 200

@pytest.mark.integration
def test_that_a_streetview_image_succeeds():
     r = client.post("/streetview")

     assert r.status_code == 200
