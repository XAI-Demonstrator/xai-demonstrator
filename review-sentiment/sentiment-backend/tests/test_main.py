import pytest
from fastapi.testclient import TestClient

from sentiment import main

client = TestClient(main.app)


@pytest.mark.integration
def test_predict_sentiment():
    test_str = "This is a test!"
    test_dict = {"text": test_str}
    response = client.post('/predict', json=test_dict)
    response_dict = response.json()

    assert response.status_code == 200
    assert "prediction" in response_dict


@pytest.mark.integration
def test_that_sentiment_is_explained():
    test_str = "This is a test!"
    test_dict = {"text": test_str}
    response = client.post('/explain', json=test_dict)
    response_dict = response.json()

    assert response.status_code == 200
    assert "explanation" in response_dict


@pytest.mark.integration
def test_that_sentiment_is_explained_with_custom_target():
    test_str = "This is a test!"
    test_dict = {"text": test_str, "target": 2}
    response = client.post('/explain', json=test_dict)
    response_dict = response.json()

    assert response.status_code == 200
    assert "explanation" in response_dict


@pytest.mark.integration
def test_that_sentiment_is_explained_with_custom_explainer():
    test_str = "This is a very good review."
    test_dict = {"text": test_str, "method": "random_words"}
    response = client.post('/explain', json=test_dict)
    response_dict = response.json()

    assert response.status_code == 200
    assert "explanation" in response_dict


def test_that_empty_text_is_not_predicted():
    response = client.post('/predict', json={"text": ""})
    assert response.status_code == 422


def test_that_empty_text_is_not_explained():
    response = client.post('/explain', json={"text": ""})
    assert response.status_code == 422


def test_that_custom_explanation_targets_outside_range_are_not_accepted():
    response = client.post('/explain', json={"text": "This is a review.", "target": 10})
    assert response.status_code == 422

    response = client.post('/explain', json={"text": "This is a review.", "target": -4})
    assert response.status_code == 422


def test_that_only_available_explainers_are_accepted(mocker):
    mocker.patch.object(main, 'EXPLAINERS', ["existing"])

    response = client.post('/explain', json={"text": "This is a stellar review.",
                                             "target": 4, "method": "unavailable"})
    assert response.status_code == 422


def test_that_the_explainer_availability_check_works(mocker):
    mocker.patch.object(main, 'EXPLAINERS', ["existing"])

    good_exp_req = main.ExplanationRequest(text="some text",
                                           target=3,
                                           method="existing")
    with pytest.raises(ValueError):
        bad_exp_req = main.ExplanationRequest(text="some text",
                                              target=3,
                                              method="unavailable")
