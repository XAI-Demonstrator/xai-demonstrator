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
    assert "prediction" in response_dict
    assert "explanation" in response_dict


@pytest.mark.integration
def test_that_sentiment_is_explained_with_custom_target():
    test_str = "This is a test!"
    test_dict = {"text": test_str, "target": 2}
    response = client.post('/explain', json=test_dict)
    response_dict = response.json()

    assert response.status_code == 200
    assert "prediction" in response_dict
    assert "explanation" in response_dict


def test_that_empty_text_is_not_predicted():
    response = client.post('/predict', json={"text": ""})
    assert response.status_code == 422


def test_that_empty_text_is_not_explained():
    response = client.post('/explain', json={"text": ""})
    assert response.status_code == 422


def test_that_custom_explanation_target_outside_range_is_not_accepted():
    response = client.post('/explain', json={"text": "This is a review.", "target": 10})
    assert response.status_code == 422

    response = client.post('/explain', json={"text": "This is a review.", "target": -4})
    assert response.status_code == 422


def test_that_availability_check_works(mocker):
    mocker.patch.object(main, 'EXPLAINERS', ["existing"])

    good_exp_req = main.ExplanationRequest(text="some text",
                                           target=3,
                                           method="existing")
    with pytest.raises(ValueError):
        bad_exp_req = main.ExplanationRequest(text="some text",
                                              target=3,
                                              method="unavailable")
