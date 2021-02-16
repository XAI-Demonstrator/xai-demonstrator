import pydantic
import pytest

from inspection.explainer.explainers import lime_


def test_that_settings_are_parsed():

    partial_settings = {
        "explainer": {
            "num_samples": 45,
            "num_features": 8000
        },
        "renderer": {
            "positive_only": True
        }
    }

    config = lime_.LIMEConfiguration(**partial_settings)

    assert config.renderer.positive_only
    assert config.explainer.num_samples == 45
    assert config.explainer.num_features == 8000


def test_that_extra_parameters_are_rejected():

    settings_with_extras = {
        "explainer": {
            "wrong": 80
        }
    }

    with pytest.raises(pydantic.ValidationError):
        _ = lime_.LIMEConfiguration(**settings_with_extras)
