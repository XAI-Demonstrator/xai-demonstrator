import aioresponses
import pytest
from fastapi.testclient import TestClient
from yarl import URL
import json

from proxy import main

client = TestClient(main.app)


@pytest.fixture
def aiomock():
    with aioresponses.aioresponses() as m:
        m.post("/record", status=200)
        yield m


def test_that_empty_call_is_passed(aiomock):
    aiomock.post("/route", status=200, payload={"my": "response"})

    response = client.post("/route")

    assert response.status_code == 200
    assert len(aiomock.requests.get(("POST", URL("/route")))) == 1


def test_that_empty_response_is_handled(aiomock):
    aiomock.post("/route", status=200)

    response = client.post("/route", json={"test": "message"})

    assert response.status_code == 200
    assert len(aiomock.requests.get(("POST", URL("/route")))) == 1


def test_that_entirely_empty_call_is_handled(aiomock):
    aiomock.post("/route", status=200)

    response = client.post("/route")

    assert response.status_code == 200
    assert len(aiomock.requests.get(("POST", URL("/route")))) == 1


def test_that_json_payload_is_passed(aiomock):
    aiomock.post("/route", status=200)

    response = client.post("/route", json={"test": "message"})

    assert response.status_code == 200
    call = aiomock.requests.get(("POST", URL("/route")))
    assert call[0].kwargs["json"] == {"test": "message"}


def test_that_form_payload_is_passed(aiomock):
    aiomock.post("/route", status=200)

    response = client.post("/route", data={"test": "message"})

    assert response.status_code == 200
    call = aiomock.requests.get(("POST", URL("/route")))[0]
    assert call.kwargs["data"] == {"test": "message"}


def test_that_json_response_is_handled(aiomock):
    aiomock.post("/route", status=200, payload={"my": "response"})

    response = client.post("/route", json={"my": "message"})

    assert response.status_code == 200
    assert response.json() == {"my": "response"}


def test_that_status_code_is_passed(aiomock):
    aiomock.post("/route", status=500)

    response = client.post("/route")

    assert response.status_code == 500


def test_that_error_message_is_passed(aiomock):
    aiomock.post("/route", status=409, payload={"msg": "Write conflict."})

    response = client.post("/route")

    assert response.status_code == 409
    assert response.json()["msg"] == "Write conflict."


def test_that_status_code_is_recorded(aiomock):
    aiomock.post("/route", status=404)

    response = client.post("/route")

    assert response.status_code == 404
    call = aiomock.requests.get(("POST", URL("/record")))[0]
    assert call.kwargs["json"]["part"]["tracked"]["response"]["status_code"] == 404


def test_that_response_is_recorded(aiomock):
    aiomock.post("/route", status=200, payload={"so": "nice", "out": "here"})

    response = client.post("/route")

    assert response.status_code == 200

    call = aiomock.requests.get(("POST", URL("/record")))[0]

    recorded_response = call.kwargs["json"]["part"]["tracked"]["response"]
    assert recorded_response["status_code"] == 200
    assert recorded_response["decoded"] == {"so": "nice", "out": "here"}

    raw_data = recorded_response["raw"]
    assert raw_data
    assert json.loads(bytes.fromhex(raw_data).decode("utf-8")) == {"so": "nice", "out": "here"}



