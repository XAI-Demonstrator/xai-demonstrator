import pytest
from fastapi.testclient import TestClient

from inspection import main

client = TestClient(main.app)


@pytest.mark.integration
def test_that_prediction_succeeds(generate_image):
    response = client.post("/predict", files={"file": generate_image(200, 300)})

    assert response.status_code == 200


@pytest.mark.integration
def test_that_explanation_succeeds(generate_image):
    r = client.post("/explain", files={"file": generate_image(110, 224)})

    assert r.status_code == 200


@pytest.mark.integration
def test_that_explanation_request_is_accepted(generate_image):
    r = client.post("/explain", files={"file": generate_image(110, 224)},
                    data={"method": "lime",
                          "settings": '{"explainer": {"num_samples": 50}}'})

    assert r.status_code == 200


def test_that_only_available_explainers_are_accepted(mocker, generate_image):
    mocker.patch("inspection.api.EXPLAINERS", ["existing"])

    response = client.post('/explain',
                           files={"file": generate_image(110, 224)},
                           data={"method": "unavailable"})

    assert response.status_code == 422


def test_that_settings_without_method_raise_error(generate_image):

    response = client.post('/explain',
                           files={"file": generate_image(110, 224)},
                           data={"settings": '{"explainer": {"samples": 5}}'})

    assert response.status_code == 400

