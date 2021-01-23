import pathlib

import pytest
from fastapi.testclient import TestClient

from inspection import main

PATH = pathlib.Path(__file__).parent

client = TestClient(main.app)


@pytest.mark.integration
def test_prediction(generate_image):
    response = client.post("/predict", files={"file": generate_image(200, 300)})

    assert response.status_code == 200


@pytest.mark.integration
def test_explanation(generate_image):
    r = client.post("/explain", files={"file": generate_image(110, 224)})

    assert r.status_code == 200
