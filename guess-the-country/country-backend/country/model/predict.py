import cv2
import numpy as np
import tensorflow as tf
import base64
import pathlib

PATH = pathlib.Path(__file__).parent

model = tf.keras.models.load_model(PATH / "my_model")


def load_image(encoded_data):
    encoded_data = str(encoded_data.split(',')[1])
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def predict_image(image, country_array):
    prediction = model.predict(image)
    result = (country_array[int(np.argmax(prediction, axis=1))]['city'])
    return result


def preprocess(img, IMG_SIZE=224):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # resize image to match model's expected sizing
    img_resize = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))
    pre_image = img_resize.reshape(-1, IMG_SIZE, IMG_SIZE, 3) / 255
    return pre_image
