import uuid
from typing import IO

import numpy as np
import tensorflow as tf
from PIL import Image
from opentelemetry import trace
from pydantic import BaseModel
from xaidemo.tracing import traced, add_span_attributes

from .model import model


# TODO: Define the content of the Prediction
class Prediction(BaseModel):
    prediction_id: uuid.UUID
    class_id: int
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
def predict(image_file: IO[bytes],
            model_: tf.keras.Model = model) -> Prediction:
    prediction_id = uuid.uuid4()
    add_span_attributes({"prediction.id": str(prediction_id)})

    input_img = Image.open(image_file)
    model_input = preprocess(input_img)

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("predict_class"):
        prediction = model_.predict(model_input)

        class_id = int(np.argmax(prediction))
        class_label = tf.keras.applications.mobilenet_v2.decode_predictions(prediction, top=1)[0][0][1]

    return Prediction(prediction_id=prediction_id,
                      class_id=class_id,
                      class_label=class_label)
