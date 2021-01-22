import uuid
from typing import IO

import numpy as np
import tensorflow as tf
from PIL import Image
from fastapi import UploadFile
from pydantic import BaseModel

from .model import model


class Prediction(BaseModel):
    prediction_id: uuid.UUID
    class_id: int
    class_label: str


# https://deeplizard.com/learn/video/OO4HD-1wRN8


def load_and_preprocess(image_file: IO[bytes]):
    img = Image.open(image_file)
    img = img.resize((224, 224), Image.NEAREST)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array[:, :, :, :3]
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array)


def predict(image_file: UploadFile,
            model_: tf.keras.Model = model) -> Prediction:
    input_img = load_and_preprocess(image_file.file)

    prediction = model_.predict(input_img)

    class_id = int(np.argmax(prediction))

    class_label = tf.keras.applications.mobilenet_v2.decode_predictions(prediction, top=1)[0][0][1]

    return Prediction(prediction_id=uuid.uuid4(),
                      class_id=class_id,
                      class_label=class_label)
