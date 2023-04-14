import cv2
import numpy as np
import tensorflow as tf
import base64
import pathlib
import uuid
from pydantic import BaseModel
from xaidemo.tracing import traced

PATH = pathlib.Path(__file__).parent
IMG_SIZE = 224
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
    prediction = process_predict(image[None,:,:,:])
    result = decode_model_output(prediction)
    return result

@traced
def preprocess(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # resize image to match model's expected sizing
    img_resize = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))
    #image = tf.keras.applications.mobilenet_v2.preprocess_input(img_resize)
    #pre_image = img_resize
    #pre_image = image.reshape(-1, IMG_SIZE, IMG_SIZE, 3)
    
    return img_resize


def process_predict(batch: np.ndarray): 
    """
    input: np array of size (batch, height, width, 3)
    output: np array of size (batch, 4) where every row represents the softmax output of a
            image inside the given batch
    """
    proc_batch = tf.keras.applications.mobilenet_v2.preprocess_input(batch)
    return model.predict(proc_batch)


MODEL_OUTPUT_MAP = ["Tel_Aviv", "Westjerusalem", "Berlin", "Hamburg"]

@traced
def decode_model_output(output: np.ndarray) -> str:
    return MODEL_OUTPUT_MAP[int(np.argmax(output, axis=1))]
