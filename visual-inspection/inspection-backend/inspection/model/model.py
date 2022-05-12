import json
from typing import Optional, Dict
import pathlib
import logging

import tensorflow as tf

from ..config import settings

logger = logging.getLogger()

PATH = pathlib.Path(__file__).parent

with open(PATH / "original_labels.json") as json_file:
    CLASS_INDEX = json.load(json_file)

with open(PATH / "german_labels.json") as json_file:
    GERMAN_LABELS = json.load(json_file)

with open(PATH / "english_labels.json") as json_file:
    ENGLISH_LABELS = json.load(json_file)


def _load_models() -> Dict[str, tf.keras.models.Model]:

    models = {}

    for model_path in (PATH / "models").iterdir():
        model_id = model_path.name

        try:
            model_obj = tf.keras.models.load_model(model_path)
        except IOError:
            logger.error(f"Failed to load model at {model_path}")
        else:
            models[model_id] = model_obj

    if not models:
        raise ValueError('Cannot find/load a single custom model. Run download_model.sh once to obtain them.')

    return models


MODELS = _load_models()

default_model = MODELS[settings.default_model]


def get_model(model_id: str) -> tf.keras.models.Model:
    try:
        return MODELS[model_id]
    except KeyError:
        raise KeyError(f"Unknown model id {model_id}. Available models are: {list(MODELS.keys())}")


def decode_predictions(prediction):
    if len(prediction.shape) != 2 or prediction.shape[1] != 1001:
        raise ValueError('`decode_predictions` expects '
                         'a batch of predictions '
                         '(i.e. a 2D array of shape (samples, 1001)). '
                         'Found array with shape: ' + str(prediction.shape))

    top_indices = prediction.argmax()
    return CLASS_INDEX.get(str(top_indices))[1]


def decode_label(prediction, language: Optional[str] = None):
    original_label = decode_predictions(prediction)
    if language is not None and language[:2] == "en":
        return ENGLISH_LABELS[original_label] if original_label in ENGLISH_LABELS\
            else "a " + original_label.replace("_", " ")
    else:
        return GERMAN_LABELS[original_label] if original_label in GERMAN_LABELS else original_label
