import pytest
from fastapi import HTTPException
import tensorflow as tf

from inspection.model import model


def test_that_finding_no_models_raises_error(tmp_path):
    models_dir = tmp_path / "models"
    models_dir.mkdir()

    with pytest.raises(ValueError):
        _ = model._load_models(tmp_path)


def test_that_broken_model_is_handled_gracefully(tmp_path):
    models_dir = tmp_path / "models"
    models_dir.mkdir()

    broken_model_dir = models_dir / "some-empty-model-dir"
    broken_model_dir.mkdir()

    with pytest.raises(ValueError):
        _ = model._load_models(tmp_path)


def test_that_missing_model_raises_exception(mocker):
    mocker.patch.object(model, "MODELS", {"some-model": None, "some-other-model": None})

    with pytest.raises(HTTPException):
        model.get_model("missing-model")


def test_that_we_can_load_savedmodel_models(tmp_path):
    models_dir = tmp_path / "models"
    models_dir.mkdir()

    mobilenet = tf.keras.applications.mobilenet_v2.MobileNetV2()
    mobilenet.save(models_dir / "my_savedmodel_model")

    assert (models_dir / "my_savedmodel_model").exists()
    assert "my_savedmodel_model" in model._load_models(tmp_path)


def test_that_we_can_load_hdf5_models(tmp_path):
    models_dir = tmp_path / "models"
    models_dir.mkdir()

    mobilenet = tf.keras.applications.mobilenet_v2.MobileNetV2()
    mobilenet.save(models_dir / "my_h5_model.h5")

    assert (models_dir / "my_h5_model.h5").exists()
    assert "my_h5_model" in model._load_models(tmp_path)
