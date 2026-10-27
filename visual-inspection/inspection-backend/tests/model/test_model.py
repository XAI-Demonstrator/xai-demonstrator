from collections import OrderedDict

import numpy as np
import pytest
import tensorflow as tf
from fastapi import HTTPException

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


def test_that_imagenet_decoder_works():
    prediction = np.zeros((1, 1001))
    prediction[0, 1] = 1.0

    label = model.decode_prediction(prediction)

    assert label == "goldfish"


def test_that_digital_education_decoder_works():
    prediction = np.zeros((1, 3))
    prediction[0, 1] = 1.0

    label = model.decode_prediction(prediction)

    assert label == "pencil"


def test_that_unknown_prediction_shape_raises_friendly_exception():
    prediction = np.zeros((1, 44))

    with pytest.raises(ValueError):
        _ = model.decode_prediction(prediction)

    prediction = np.zeros((5, 1001))

    with pytest.raises(ValueError):
        _ = model.decode_prediction(prediction)


def test_that_index_model_paths_maps_ids_to_paths(tmp_path):
    models_dir = tmp_path / "models"
    models_dir.mkdir()
    (models_dir / "model_a").mkdir()
    (models_dir / "model_b.h5").write_text("x")

    paths = model._index_model_paths(tmp_path)

    assert set(paths) == {"model_a", "model_b"}
    assert paths["model_a"] == models_dir / "model_a"
    assert paths["model_b"] == models_dir / "model_b.h5"


def test_that_index_model_paths_is_empty_when_dir_missing(tmp_path):
    assert model._index_model_paths(tmp_path) == {}


def test_that_lazy_get_loads_on_first_access_then_caches(mocker):
    loader = mocker.Mock(side_effect=lambda path: f"loaded:{path}")
    paths = {"model_a": "/p/a"}
    cache = OrderedDict()

    first = model._get_or_load("model_a", paths, cache, 8, loader)
    second = model._get_or_load("model_a", paths, cache, 8, loader)

    assert first == "loaded:/p/a"
    assert second is first
    loader.assert_called_once()


def test_that_lazy_get_evicts_least_recently_used(mocker):
    loader = mocker.Mock(side_effect=lambda path: path)
    paths = {f"model_{i}": f"/p/{i}" for i in range(5)}
    cache = OrderedDict()

    for i in range(3):
        model._get_or_load(f"model_{i}", paths, cache, 2, loader)

    assert set(cache) == {"model_1", "model_2"}


def test_that_lazy_get_stays_bounded_over_many_rounds(mocker):
    loader = mocker.Mock(side_effect=lambda path: path)
    paths = {f"model_{i}": f"/p/{i}" for i in range(40)}
    cache = OrderedDict()

    for r in range(200):
        model._get_or_load(f"model_{r % 40}", paths, cache, 8, loader)

    assert len(cache) == 8


def test_that_lazy_get_reloads_an_evicted_model(mocker):
    loader = mocker.Mock(side_effect=lambda path: path)
    paths = {f"model_{i}": f"/p/{i}" for i in range(5)}
    cache = OrderedDict()

    for i in range(3):
        model._get_or_load(f"model_{i}", paths, cache, 2, loader)
    model._get_or_load("model_0", paths, cache, 2, loader)

    assert loader.call_count == 4


def test_that_recently_used_model_survives_eviction(mocker):
    loader = mocker.Mock(side_effect=lambda path: path)
    paths = {f"model_{i}": f"/p/{i}" for i in range(5)}
    cache = OrderedDict()

    model._get_or_load("model_0", paths, cache, 2, loader)
    model._get_or_load("model_1", paths, cache, 2, loader)
    model._get_or_load("model_0", paths, cache, 2, loader)
    model._get_or_load("model_2", paths, cache, 2, loader)

    assert "model_0" in cache
    assert "model_1" not in cache
    assert "model_2" in cache


def test_that_lazy_get_raises_for_unknown_model(mocker):
    loader = mocker.Mock()
    cache = OrderedDict()

    with pytest.raises(HTTPException):
        model._get_or_load("missing", {"model_a": "/p/a"}, cache, 8, loader)

    loader.assert_not_called()
