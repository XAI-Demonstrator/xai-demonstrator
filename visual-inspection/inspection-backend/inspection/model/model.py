import json
import logging
import pathlib
from collections import OrderedDict
from typing import Optional, Dict

import tensorflow as tf
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from ..config import settings

logger = logging.getLogger()

PATH = pathlib.Path(__file__).parent

with open(PATH / "original_labels.json") as json_file:
    IMAGENET_LABELS = json.load(json_file)

with open(PATH / "german_labels.json") as json_file:
    GERMAN_LABELS = json.load(json_file)

with open(PATH / "english_labels.json") as json_file:
    ENGLISH_LABELS = json.load(json_file)

DIGITAL_EDUCATION_LABELS = {0: "cellular_telephone", 1: "pencil", 2: "cup"}


def _load_models(path: pathlib.Path = PATH) -> Dict[str, tf.keras.models.Model]:
    models = {}

    for model_path in (path / "models").iterdir():
        model_id = model_path.with_suffix('').name

        try:
            model_obj = tf.keras.models.load_model(model_path)
        except IOError:
            logger.error(f"Failed to load model at {model_path}")
        else:
            models[model_id] = model_obj

    if not models:
        raise ValueError('Cannot find/load a single custom model. Run download_model.sh once to obtain them.')

    return models


def _index_model_paths(path: pathlib.Path = PATH) -> Dict[str, pathlib.Path]:
    """Map each model id to its path WITHOUT loading the model (cheap, no TensorFlow)."""
    index = {}
    models_dir = path / "models"
    if models_dir.exists():
        for model_path in models_dir.iterdir():
            index[model_path.with_suffix('').name] = model_path
    return index


if settings.lazy_models:
    MODEL_PATHS = _index_model_paths()
    MODELS: "OrderedDict[str, tf.keras.models.Model]" = OrderedDict()

    default_model = None

    def get_model(model_id: str) -> tf.keras.models.Model:
        if model_id in MODELS:
            MODELS.move_to_end(model_id)
            return MODELS[model_id]

        if model_id not in MODEL_PATHS:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                                detail=f"Unknown model id {model_id}. "
                                       f"Available models are: {sorted(MODEL_PATHS)}")

        model_obj = tf.keras.models.load_model(MODEL_PATHS[model_id])
        MODELS[model_id] = model_obj
        MODELS.move_to_end(model_id)
        while len(MODELS) > max(1, settings.model_cache_limit):
            MODELS.popitem(last=False)
        return model_obj

else:
    # Eager loading (default): load all models at startup — unchanged behavior for visual-inspection.
    MODELS = _load_models()

    default_model = MODELS[settings.default_model]

    def get_model(model_id: str) -> tf.keras.models.Model:
        try:
            return MODELS[model_id]
        except KeyError:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                                detail=f"Unknown model id {model_id}. Available models are: {list(MODELS.keys())}")


def decode_prediction(prediction) -> str:
    if len(prediction.shape) != 2 or prediction.shape[0] != 1 or \
            (prediction.shape[1] != 3 and prediction.shape[1] != 1001):
        raise ValueError('`decode_predictions` expects a single prediction '
                         '(i.e., a 2D array of shape (1, 3) or (1, 1001). '
                         'Found array with shape: ' + str(prediction.shape))

    if prediction.shape[1] == 3:
        return DIGITAL_EDUCATION_LABELS[prediction.argmax()]
    else:
        return IMAGENET_LABELS.get(str(prediction.argmax()))[1]


def decode_label(prediction, language: Optional[str] = None):
    original_label = decode_prediction(prediction)
    if language is not None and language[:2] == "en":
        return ENGLISH_LABELS[original_label] if original_label in ENGLISH_LABELS \
            else "a " + original_label.replace("_", " ")
    else:
        return GERMAN_LABELS[original_label] if original_label in GERMAN_LABELS else original_label
