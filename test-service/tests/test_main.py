from fastapi.testclient import TestClient

from sentiment.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200


def test_predict_sentiment():
    test_str = "This is a test!"
    test_dict = {"text": test_str}
    response = client.post('/predict', json=test_dict)
    response_dict = response.json()

    assert response.status_code == 200
    assert "prediction" in response_dict


def test_explain_sentiment():
    test_str = "This is a test!"
    test_dict = {"text": test_str}
    response = client.post('/explain', json=test_dict)
    response_dict = response.json()

    assert response.status_code == 200
    assert "prediction" in response_dict
    assert "explanation" in response_dict


def test_that_empty_prediction_passes():
    response = client.post('/predict', json={"text": ""})
    assert response.status_code == 200


def test_that_empty_explanation_passes():
    response = client.post('/predict', json={"text": ""})
    assert response.status_code == 200

