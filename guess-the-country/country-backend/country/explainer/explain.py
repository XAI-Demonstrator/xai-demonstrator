import base64
import uuid

import cv2
import numpy as np
from pydantic import BaseModel
from visualime.explain import explain_classification, render_explanation
from xaidemo.tracing import traced

from ..model.predict import model, load_image, preprocess


class Explanation(BaseModel):
    explanation_id: uuid.UUID
    image: bytes


@traced
def explain(data):
    encoded_data = str(data)
    image = load_image(encoded_data)
    pre_image = preprocess(img=image)

    explanation = explain_cnn(pre_image, model)
    explanation_id = uuid.uuid4()

    encoded_image_string = convert_explanation(explanation)
    encoded_bytes = bytes("data:image/png;base64,",
                          encoding="utf-8") + encoded_image_string
    return Explanation(
        explanation_id=explanation_id,
        image=encoded_bytes
    )


@traced
def convert_explanation(explanation):
    image = np.array(explanation, dtype="float32")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(image_rgb, (448, 448),
                             interpolation=cv2.INTER_CUBIC)
    retval, buffer = cv2.imencode('.png', img_resized)
    encoded_image_string = base64.b64encode(buffer)
    return encoded_image_string


@traced
def explain_cnn(image, model_=model):
    segment_mask, segment_weights = explain_classification(image=image,
                                                           segmentation_method="felzenszwalb",
                                                           segmentation_settings={},
                                                           predict_fn=model_.predict_,
                                                           num_of_samples=500,
                                                           p=0.9)

    return render_explanation(image, segment_mask, segment_weights, positive="violet", coverage=0.15, opacity=0.5)
