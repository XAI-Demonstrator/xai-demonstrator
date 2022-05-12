import pytest

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

