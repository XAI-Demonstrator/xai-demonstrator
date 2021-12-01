import json
import pathlib

import tensorflow as tf

PATH = pathlib.Path(__file__).parent

with open(PATH / "original_labels.json") as json_file:
    CLASS_INDEX = json.load(json_file)

with open(PATH / "german_labels.json") as json_file:
    GERMAN_LABELS = json.load(json_file)

try:
    model = tf.keras.models.load_model(PATH / "my_model")
except IOError:
    raise IOError('Cannot find custom model. Run download_model.sh once to obtain it.')
except tf.errors.AlreadyExistsError:
    print("DEBUG flaky test on GitHub Actions")


def decode_predictions(prediction):
    if len(prediction.shape) != 2 or prediction.shape[1] != 1001:
        raise ValueError('`decode_predictions` expects '
                         'a batch of predictions '
                         '(i.e. a 2D array of shape (samples, 1001)). '
                         'Found array with shape: ' + str(prediction.shape))

    top_indices = prediction.argmax()
    return CLASS_INDEX.get(str(top_indices))[1]


def decode_label(prediction):
    original_label = decode_predictions(prediction)
    return GERMAN_LABELS[original_label] if original_label in GERMAN_LABELS else original_label
