import pathlib

import pytest
from fastapi.testclient import TestClient

from inspection import main

PATH = pathlib.Path(__file__).parent

client = TestClient(main.app)


@pytest.mark.integration
def test_prediction(dummy_image):
    response = client.post("/predict", files={"file": dummy_image})
    response_dict = response.json()

    assert response.status_code == 200
    assert "class_id" in response_dict


@pytest.mark.integration
def test_explanation(dummy_image):
    r = client.post("/explain", files={"file": dummy_image})

    assert r.status_code == 200
