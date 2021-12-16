import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from xaidemo import tracing, tracking
from xaidemo.tracking.config import TrackingSettings
from xaidemo.tracking.record import record_data, settings
from yarl import URL

tracing.set_up()


@pytest.fixture
def test_client(mocker):
    mocker.patch.object(tracking, "settings", new=TrackingSettings(experiment=True,
                                                                   collector_url="tmp"))

    app = FastAPI()
    tracking.instrument_app(app)

    @app.post("/test")
    def route():
        record_data("test_key", {"my": "test_value"})
        record_data("other_key", {"my": "big_house"})

    tracing.instrument_app(app)

    yield TestClient(app)


def test_that_data_is_sent_to_collector(aiomock, mocker, test_client):
    mocker.patch.object(settings, "experiment", new=True)
    mocker.patch.object(settings, "collector_url", new="http://collector")
    assert settings.experiment
    aiomock.post(settings.collector_url + "/record", status=200, repeat=True)

    test_client.post("/test")

    calls = aiomock.requests.get(("POST", URL(settings.collector_url + "/record")))
    assert len(calls) == 2


def test_that_collector_timeout_is_handled_gracefully(aiomock, mocker, test_client):
    mocker.patch.object(settings, "experiment", new=True)
    mocker.patch.object(settings, "collector_url", new="http://collector")
    assert settings.experiment
    aiomock.post(settings.collector_url + "/record", timeout=True, repeat=True)

    test_client.post("/test")

    calls = aiomock.requests.get(("POST", URL(settings.collector_url + "/record")))
    assert len(calls) == 2


def test_that_experiments_can_be_turned_off(aiomock, mocker, test_client):
    mocker.patch.object(settings, "experiment", new=False)
    mocker.patch.object(settings, "collector_url", new="http://collector")
    assert not settings.experiment

    aiomock.post(settings.collector_url + "/record", status=200, repeat=True)

    test_client.post("/test")

    calls = aiomock.requests.get(("POST", URL(settings.collector_url + "/record")))
    assert not calls
