import pytest

from fastapi.testclient import TestClient

from inspection import api, main

FULL_TYPED_SETTINGS = '''{"settings": {"explainer": {
                                        "int_compatible": "50",
                                         "float_compatible": "50.5",
                                         "bool_compatible": "false",
                                         "proper_bool": true,
                                         "str_only": "word",
                                         "proper_int": 10,
                                         "proper_float": 2.5}}}'''


def test_explanation_request_parses_typed_values():
    s = api.ExplanationRequest.parse_raw(FULL_TYPED_SETTINGS)

    explainer = s.settings["explainer"]
    assert isinstance(explainer["int_compatible"], int)
    assert explainer["int_compatible"] == 50
    assert isinstance(explainer["float_compatible"], float)
    assert explainer["float_compatible"] == 50.5
    assert isinstance(explainer["str_only"], str)
    assert explainer["str_only"] == "word"
    assert isinstance(explainer["proper_int"], int)
    assert explainer["proper_int"] == 10
    assert isinstance(explainer["proper_float"], float)
    assert explainer["proper_float"] == 2.5
    assert isinstance(explainer["proper_bool"], bool)
    assert explainer["proper_bool"]
    assert isinstance(explainer["bool_compatible"], bool)
    assert not explainer["bool_compatible"]


client = TestClient(main.app)


def test_that_language_is_passed(generate_image, mocker):
    p = mocker.patch.object(api, "predict")

    response = client.post("/predict", files={"file": generate_image(200, 300)}, data={"language": "en"})

    assert response.status_code == 200
    args, kwargs = p.call_args_list[0]
    assert "language" in kwargs
    assert kwargs["language"] == "en"


def test_that_model_id_is_passed_for_prediction(generate_image, mocker):
    p = mocker.patch.object(api, "predict")

    response = client.post("/predict", files={"file": generate_image(200, 300)}, data={"model_id": "this-is-a-model"})

    assert response.status_code == 200
    args, kwargs = p.call_args_list[0]
    assert "model_id" in kwargs
    assert kwargs["model_id"] == "this-is-a-model"
