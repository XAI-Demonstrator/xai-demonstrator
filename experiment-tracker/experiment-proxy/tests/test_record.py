import itertools

import pytest
from pydantic import ValidationError

from proxy.record import RequestData, ResponseData, prepare_record, TrackedData


def test_that_request_can_be_empty():
    _ = RequestData()


def test_that_request_must_contain_all_values():
    data = {
        "raw": "a1b2",
        "content_type": "application/json",
        "decoded": {"msg": "content"}
    }

    for a, b in itertools.combinations(data.items(), 2):
        with pytest.raises(ValidationError):
            kwargs = dict((a, b))
            _ = RequestData(**kwargs)

    _ = RequestData(**data)


def test_that_response_must_not_be_empty():
    with pytest.raises(ValidationError):
        _ = ResponseData()


def test_that_response_has_to_contain_at_least_status_code():
    _ = ResponseData(status_code=200)


def test_that_both_raw_and_decoded_must_be_set():
    raw_ = "12345"
    decoded = {"my": "value"}

    with pytest.raises(ValidationError):
        _ = ResponseData(status_code=200, raw=raw_)

    with pytest.raises(ValidationError):
        _ = ResponseData(status_code=200, decoded=decoded)

    _ = ResponseData(status_code=200, raw=raw_, decoded=decoded)


def test_that_service_and_provider_are_set():
    tracked_data = TrackedData(request=RequestData(), response=ResponseData(status_code=200))
    partial_record_request = prepare_record("predict", "demo", tracked_data)

    assert partial_record_request.source.service == "backend-under-test"
    assert partial_record_request.source.provider == "proxy-under-test"

