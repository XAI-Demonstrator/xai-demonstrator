import itertools

import aioresponses
import pytest
from pydantic import ValidationError
from yarl import URL

from proxy.record import RequestData, ResponseData, record_data


def test_that_request_can_be_empty():
    request = RequestData()


def test_that_request_must_contain_all_values():
    data = {
        "raw": "a1b2",
        "content_type": "application/json",
        "decoded": {"msg": "content"}
    }

    for a, b in itertools.combinations(data.items(), 2):
        with pytest.raises(ValidationError):
            kwargs = dict((a, b))
            request = RequestData(**kwargs)

    request = RequestData(**data)


def test_that_response_must_not_be_empty():
    with pytest.raises(ValidationError):
        response = ResponseData()


def test_that_response_has_to_contain_at_least_status_code():
    response = ResponseData(status_code=200)


def test_that_both_raw_and_decoded_must_be_set():
    raw_ = "12345"
    decoded = {"my": "value"}

    with pytest.raises(ValidationError):
        response = ResponseData(status_code=200, raw=raw_)

    with pytest.raises(ValidationError):
        response = ResponseData(status_code=200, decoded=decoded)

    response = ResponseData(status_code=200, raw=raw_, decoded=decoded)


@pytest.fixture
def aiomock():
    with aioresponses.aioresponses() as m:
        yield m


@pytest.mark.asyncio
async def test_that_key_cannot_equal_id():
    with pytest.raises(ValueError):
        await record_data("123", "/call", key="id", value={"big": "data"})


@pytest.mark.asyncio
async def test_that_data_is_sent(aiomock):
    aiomock.post("/record", status=202)

    await record_data("abc123", "/call", key="tracked", value={"small": "payload"})

    call = aiomock.requests.get(("POST", URL("/record")))[0]
    assert call.kwargs["json"]["id"] == "abc123"
    assert call.kwargs["json"]["part"] == {"tracked": {"small": "payload"}}
