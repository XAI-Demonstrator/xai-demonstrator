import uuid
from typing import Callable, IO

import numpy as np
import tensorflow as tf
from PIL import Image
from pydantic import BaseModel
from xaidemo.tracing import add_span_attributes, traced

from .model import decode_label, model


class Prediction(BaseModel):
    prediction_id: uuid.UUID
    class_label: str


@traced
def preprocess(img: Image) -> np.ndarray:
    add_span_attributes({"image.size": img.size})

    # cf. https://deeplizard.com/learn/video/OO4HD-1wRN8
    img = img.resize((224, 224), Image.BICUBIC)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array[:, :, :, :3]
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array)


@traced
def predict_class(model_input: np.ndarray,
                  model_: tf.keras.Model = model,
                  decode_label_: Callable[[np.ndarray], str] = decode_label) -> str:
    prediction = model_.predict(model_input)

    class_label = decode_label_(prediction)

    return class_label


@traced
def predict(image_file: IO[bytes],
            ) -> Prediction:
    prediction_id = uuid.uuid4()
    add_span_attributes({"prediction.id": str(prediction_id)})

    input_img = Image.open(image_file)
    model_input = preprocess(input_img)

    class_label = predict_class(model_input)

    return Prediction(prediction_id=prediction_id,
                      class_label=class_label)
