from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"msg": "Welcome to my service!"}


def test_predict_sentiment():
    test_str = "This is a test!"
    test_dict = {"payload": test_str}
    response = client.post('/predict', params=test_dict)
    response_dict = response.json()

    assert response.status_code == 201
    assert "prediction" in response_dict
    assert response_dict["prediction"] in ["positive", "neutral", "negative"]


def test_explain_sentiment():
    test_str = "This is a test!"
    test_dict = {"payload": test_str}
    response = client.post('/explain', params=test_dict)
    response_dict = response.json()

    assert response.status_code == 201
    assert "prediction" in response_dict
    assert "explanation" in response_dict
    assert response_dict["prediction"] in ["positive", "neutral", "negative"]
    assert response_dict["explanation"] in test_str.split(" ")