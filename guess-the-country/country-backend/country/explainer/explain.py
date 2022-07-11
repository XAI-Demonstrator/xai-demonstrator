import base64
import logging

import cv2
import numpy as np
from ..model.predict import model, load_image, preprocess
from pydantic import BaseModel
import uuid
from xaidemo.tracing import traced
from .new_lime_ import explain_image
import tensorflow as tf
from visualime.explain import explain_classification, render_explanation


class Explanation(BaseModel):
    explanation_id: uuid.UUID
    image: bytes


@traced
def explain(data):
    encoded_data = str(data)
    image = load_image(encoded_data)
    pre_image = preprocess(image)
    explanation = explain_cnn(pre_image, model)
    explain_id = uuid.uuid4()
    encoded_image_string = convert_explanation(explanation)
    encoded_bytes = bytes("data:image/png;base64,",
                          encoding="utf-8") + encoded_image_string
    return Explanation(
        explanation_id=explain_id,
        image=encoded_bytes
    )


@traced
def convert_explanation(explanation):
    image = np.array(explanation)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(image_rgb, (448, 448),
                             interpolation=cv2.INTER_CUBIC)
    retval, buffer = cv2.imencode('.png', img_resized)
    encoded_image_string = base64.b64encode(buffer)
    return encoded_image_string


@traced
def explain_cnn(image, model):
    def _predict_fn(img):
        IMG_SIZE = 224
        return model.predict(
            tf.keras.applications.mobilenet_v2.preprocess_input(img.reshape(-1, IMG_SIZE, IMG_SIZE, 3)))

    segment_mask, segment_weights = explain_classification(image=image, segmentation_method="felzenszwalb",
                                                           predict_fn=_predict_fn, num_of_samples=275, p=0.75)

    return render_explanation(image, segment_mask, segment_weights, positive="violet", coverage=0.05, opacity=0.2)
