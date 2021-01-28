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
                          "settings": {"num_samples": 50}})

    assert r.status_code == 200


def test_explanation_request_parses_numeric_values():
    r = main.ExplanationRequest(settings={"int_compatible": "50",
                                          "float_compatible": "50.5",
                                          "str_only": "word",
                                          "proper_int": 10,
                                          "proper_float": 2.5})

    assert isinstance(r.settings["int_compatible"], int)
    assert r.settings["int_compatible"] == 50
    assert isinstance(r.settings["float_compatible"], float)
    assert r.settings["float_compatible"] == 50.5
    assert isinstance(r.settings["str_only"], str)
    assert r.settings["str_only"] == "word"
    assert isinstance(r.settings["proper_int"], int)
    assert r.settings["proper_int"] == 10
    assert isinstance(r.settings["proper_float"], float)
    assert r.settings["proper_float"] == 2.5


def test_that_only_available_explainers_are_accepted(mocker, generate_image):
    mocker.patch.object(main, 'EXPLAINERS', ["existing"])

    response = client.post('/explain',
                           files={"file": generate_image(110, 224)},
                           data={"method": "unavailable"})

    assert response.status_code == 422
