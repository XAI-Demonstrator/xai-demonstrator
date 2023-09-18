import pathlib
import uuid
from typing import IO

import numpy as np
import tensorflow as tf
from PIL import Image
from pydantic import BaseModel
from xaidemo.tracing import traced

PATH = pathlib.Path(__file__).parent

MODEL_INPUT_IMG_SIZE = 224
MODEL_OUTPUT_MAP = ["Tel Aviv", "West Jerusalem", "Berlin", "Hamburg"]

model = tf.keras.models.load_model(PATH / "my_model")


class Prediction(BaseModel):
    prediction_id: uuid.UUID
    city: str


@traced
def predict_city(image_file: IO[bytes]) -> Prediction:
    image = Image.open(image_file)
    preprocessed_image = preprocess(image)
    city = predict_image(image=preprocessed_image)
    return Prediction(prediction_id=uuid.uuid4(),
                      city=city)


@traced
def predict_image(image: np.ndarray):
    prediction = model.predict(image)
    result = decode_model_output(prediction)
    return result


@traced
def preprocess(image: Image) -> np.ndarray:
    image = image.resize((MODEL_INPUT_IMG_SIZE, MODEL_INPUT_IMG_SIZE), Image.Resampling.BICUBIC)

    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array[:, :, :, :3]
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array)


@traced
def decode_model_output(output: np.ndarray) -> str:
    return MODEL_OUTPUT_MAP[int(np.argmax(output, axis=1))]
