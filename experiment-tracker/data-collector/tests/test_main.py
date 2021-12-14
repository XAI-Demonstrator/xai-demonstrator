import uuid
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from collector import main


@pytest.fixture()
def client():
    with patch.object(main, 'repo', new_callable=dict):
        yield TestClient(main.app)


my_id = str(uuid.uuid4())

example = {
    "id": my_id,
    "source": {
        "name": "test-service"
    },
    "part": {
        "demo": {
            "msg": "hello world"
        }
    }
}


def test_that_request_is_recorded(client):
    response = client.post("/record", json=example)
    assert response.status_code == 200


def test_that_record_can_be_retrieved(client):
    response = client.post("/record", json=example)
    assert response.status_code == 200

    response = client.get(f"/get/{my_id}")

    record = response.json()
    del record["timestamp"]

    assert response.status_code == 200
    assert record["data"] == example["part"]


def test_that_request_for_missing_record_is_handled_gracefully(client):
    response = client.get(f"/get/{str(uuid.uuid4())}")

    assert response.status_code == 404


def test_that_dump_is_created(client):
    for _ in range(10):
        record = example.copy()
        record["id"] = str(uuid.uuid4())
        _ = client.post("/record", json=record)

    response = client.get("/dump")

    assert response.status_code == 200
    assert len(response.json()["records"]) == 10
