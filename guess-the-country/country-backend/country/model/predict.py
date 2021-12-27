import cv2
import numpy as np
import tensorflow as tf
import base64

def load_model():
    model = tf.keras.models.load_model("model_x2.model")
    return model

def load_image(file):
    encoded_data = str(file.file.read())
    #image = str(image)
    encoded_data = encoded_data.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img 

def predict_image(image, model):
    CATEGORIES = ["Tel-Aviv", "Berlin", "Hamburg"]
    prediction = model.predict(image)
    result = (CATEGORIES[int(np.argmax(prediction, axis=1))])
    return result


def preprocess(img):
    IMG_SIZE = 224 
    new_array = cv2.resize(img, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing
    new_data = new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3) / 255
    return new_data