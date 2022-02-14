from lime import lime_image
from skimage.segmentation import mark_boundaries
import base64
import cv2
import numpy as np
from ..model.predict import model, load_image, preprocess
from pydantic import BaseModel
import uuid
from xaidemo.tracing import traced
from .new_lime_ import explain_image



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
    image = (explanation * 255).astype(np.uint8)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(image_rgb, (448, 448),
                             interpolation=cv2.INTER_CUBIC)
    retval, buffer = cv2.imencode('.png', img_resized)
    encoded_image_string = base64.b64encode(buffer)
    return encoded_image_string


@traced
def explain_cnn(img, model):
    return explain_image(img=img, seg_method="felzenszwalb", seg_settings={}, num_of_samples=200, samples_p=0.5,
                         model_=model, threshold=0.3, volume=45, colour="red")
