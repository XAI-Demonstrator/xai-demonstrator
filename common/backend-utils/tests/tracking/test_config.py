import pydantic
import pytest

from xaidemo.tracking import config


def test_that_not_setting_anything_works():
    settings = config.TrackingSettings()

    assert not settings.experiment


def test_that_experiment_requires_collector():
    with pytest.raises(pydantic.ValidationError):
        _ = config.TrackingSettings(experiment=True)

    settings = config.TrackingSettings(experiment=True,
                                       collector_url="https://track.xaidemo.de")

    assert settings.experiment
