from io import BytesIO
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications.imagenet_utils import decode_predictions

def load_model():
    model = tf.keras.models.load_model("model_mnv2.model")
    return model

def predict_image(image, model):
    CATEGORIES = ["Tel-Aviv", "Berlin"]
    prediction = model.predict(image)
    result = CATEGORIES[int(prediction[0][0] >= 0.5)]
    print(result)
    return result


def preprocess(image: Image.Image):
    image = np.asarray(image.resize((224, 224)))[..., :3]
    image = np.expand_dims(image, 0)
    image = image / 224

    return image

def preprocess2(img_array):
    IMG_SIZE = 224  # 50 in txt-based
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3) / 224  # return the image with shaping that TF wants.

def read_imagefile(file):
    image = Image.open(BytesIO(file))
    return image


def read_imagefile2(file):
    nparr = np.fromstring(file, np.uint8)
    img_array = cv2.cvtColor(cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR), cv2.COLOR_BGR2RGB)   # read in the image, convert to grayscale
    return img_array

def prepare(filepath):
    IMG_SIZE = 224  # 50 in txt-based
    img_array = cv2.cvtColor(cv2.imread(filepath, cv2.IMREAD_ANYCOLOR), cv2.COLOR_BGR2RGB)   # read in the image, convert to grayscale
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3) / 224  # return the image with shaping that TF wants.
