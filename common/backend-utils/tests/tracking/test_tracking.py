from fastapi import FastAPI
from fastapi.testclient import TestClient
from xaidemo import tracing
from xaidemo.tracking.middleware import ExperimentTrackerMiddleware
from xaidemo.tracking.record import record_data, settings
from yarl import URL

tracing.set_up()

app = FastAPI()
app.add_middleware(ExperimentTrackerMiddleware)


@app.post("/test")
def route():
    record_data("test_key", {"my": "test_value"})
    record_data("other_key", {"my": "big_house"})


tracing.instrument_app(app)

test_client = TestClient(app)


def test_that_data_is_sent_to_collector(aiomock):
    assert settings.experiment
    aiomock.post(settings.collector_url + "/record", status=200, repeat=True)

    test_client.post("/test")

    calls = aiomock.requests.get(("POST", URL(settings.collector_url + "/record")))
    assert len(calls) == 2


def test_that_collector_timeout_is_handled_gracefully(aiomock):
    assert settings.experiment
    aiomock.post(settings.collector_url + "/record", timeout=True, repeat=True)

    test_client.post("/test")

    calls = aiomock.requests.get(("POST", URL(settings.collector_url + "/record")))
    assert len(calls) == 2


def test_that_experiments_can_be_turned_off(aiomock, mocker):
    mocker.patch.object(settings, "experiment", new=False)
    assert not settings.experiment

    aiomock.post(settings.collector_url + "/record", status=200, repeat=True)

    test_client.post("/test")

    calls = aiomock.requests.get(("POST", URL(settings.collector_url + "/record")))
    assert not calls
