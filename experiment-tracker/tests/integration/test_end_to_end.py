import time
import uuid

import requests
from opentelemetry import trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from xaidemo.tracking.record import get_record_id

RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)


def test_that_record_id_is_propagated(proxy, collector):
    with tracer.start_as_current_span(name="root_span"):
        record_id = get_record_id()
        my_id = str(uuid.uuid4())

        r = requests.post(proxy + "/json", json={"find": my_id})

        assert r.status_code == 200
        print(r.json())

        # wait for collector to receive data
        time.sleep(10)

        r = requests.get(collector + "/dump")

        assert r.status_code == 200

        records = r.json()["records"]

        for record in records:
            if "tracked" not in record["data"]:
                continue

            if "find" in record["data"]["tracked"]["data"]["request"]["decoded"]:
                if record["data"]["tracked"]["data"]["request"]["decoded"]["find"] == my_id:
                    break
        else:
            raise AssertionError("Did not find entry")

        assert record["id"] == record_id


def test_that_new_contexts_are_initialized():
    with tracer.start_as_current_span(name="root_span"):
        first_id = get_record_id()

    with tracer.start_as_current_span(name="root_span"):
        second_id = get_record_id()

    assert first_id != second_id
