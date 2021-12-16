import uuid
from unittest.mock import patch
from copy import deepcopy

import pytest
from fastapi.testclient import TestClient
from collector import main
from xaidemo.tracking.data_models import PartialRecordRequest


@pytest.fixture()
def client():
    with patch.object(main, 'repo', new_callable=dict):
        yield TestClient(main.app)


my_id = str(uuid.uuid4())

example = {
    "id": my_id,
    "source": {
        "service": "test-service",
        "provider": "test-service"
    },
    "part": {
        "demo": {
            "msg": "hello world",
            "number": 1234
        }
    },
    "label": "test"
}


def test_that_example_is_valid():
    _ = PartialRecordRequest(**example)


def test_that_request_is_recorded(client):
    response = client.post("/record", json=example)
    assert response.status_code == 200


def test_that_updates_are_recorded(client):
    _ = client.post("/record", json=example)

    next_update = deepcopy(example)
    del next_update["part"]["demo"]
    next_update["part"]["test"] = {"msg": "and again"}

    response = client.post("/record", json=next_update)

    assert response.status_code == 200


def test_that_same_key_cannot_be_recorded_twice(client):
    _ = client.post("/record", json=example)
    response = client.post("/record", json=example)

    assert response.status_code == 409


def test_that_source_service_cannot_change(client):
    _ = client.post("/record", json=example)
    next_update = deepcopy(example)
    next_update["source"]["service"] = "some-other-service"

    response = client.post("/record", json=next_update)

    assert response.status_code == 409


def test_that_record_can_be_retrieved(client):
    response = client.post("/record", json=example)
    assert response.status_code == 200

    response = client.get(f"/get/{my_id}")

    record = response.json()

    assert response.status_code == 200
    assert record["data"]["demo"]["data"] == example["part"]["demo"]
    assert record["data"]["demo"]["provider"] == "test-service"


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
