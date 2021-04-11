import uuid
from unittest.mock import patch
import json
import pytest
from fastapi.testclient import TestClient

from tracker import main


@pytest.fixture()
def client():
    with patch.object(main, 'repo', new_callable=dict):
        yield TestClient(main.app)


my_id = str(uuid.uuid4())

example = {
    "service_name": "test-service",
    "request_id": my_id,
    "request": {
        "text": "This is a test!"
    },
    "response": {
        "prediction_id": my_id,
        "class_name": "Camera",
        "class_id": 4
    }
}


def test_that_request_is_recorded(client):
    response = client.put("/record", json=example)

    assert response.status_code == 201


def test_that_request_can_be_retrieved(client):
    _ = client.put("/record", json=example)

    response = client.get(f"/get/{my_id}")

    request = response.json()
    del request["timestamp"]

    assert response.status_code == 200
    assert request == example


def test_that_request_for_missing_record_is_handled_gracefully(client):
    response = client.get(f"/get/{str(uuid.uuid4())}")

    assert response.status_code == 404
