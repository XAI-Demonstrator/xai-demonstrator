import logging

import cv2
import numpy as np
import tensorflow as tf
import base64
import pathlib
import uuid
from pydantic import BaseModel
from xaidemo.tracing import traced

PATH = pathlib.Path(__file__).parent

model = tf.keras.models.load_model(PATH / "my_model")

class Prediction(BaseModel):
    prediction_id: uuid.UUID
    class_label: str

@traced
def prediction(input):
    encoded_data = str(input)
    image = load_image(encoded_data)
    pre_image = preprocess(image)
    prediction_id = uuid.uuid4()
    label = predict_image(image=pre_image)
    return Prediction(prediction_id=prediction_id,
                      class_label=label)

@traced
def load_image(encoded_data):
    encoded_data = str(encoded_data)
    encoded_data = encoded_data.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

@traced
def predict_image(image):
    prediction = model.predict(image[None, :, :, :])
    result = decode_model_output(prediction)
    return result

@traced
def preprocess(img, IMG_SIZE=224):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # resize image to match model's expected sizing
    img_resize = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))
    return img_resize


MODEL_OUTPUT_MAP = ["Tel_Aviv", "Westjerusalem", "Berlin", "Hamburg"]

@traced
def decode_model_output(output: np.ndarray) -> str:
    return MODEL_OUTPUT_MAP[int(np.argmax(output, axis=1))]
