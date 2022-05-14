import pytest
from fastapi import HTTPException

from inspection.model import model


def test_that_finding_no_models_raises_error(mocker, tmp_path):
    models_dir = tmp_path / "models"
    models_dir.mkdir()

    p = mocker.patch.object(model, "PATH")
    p.return_value = tmp_path

    with pytest.raises(ValueError):
        _ = model._load_models()


def test_that_broken_model_is_handled_gracefully(mocker, tmp_path):
    models_dir = tmp_path / "models"
    models_dir.mkdir()

    broken_model_dir = models_dir / "some-empty-model-dir"
    broken_model_dir.mkdir()

    p = mocker.patch.object(model, "PATH")
    p.return_value = tmp_path

    m = mocker.patch.object(model, "tf")
    m.side_effect = IOError

    with pytest.raises(ValueError):
        _ = model._load_models()


def test_that_missing_model_raises_exception(mocker):
    mocker.patch.object(model, "MODELS", {"some-model": None, "some-other-model": None})

    with pytest.raises(HTTPException):
        model.get_model("missing-model")
