import base64
import io
import uuid
from typing import IO

import numpy as np
from PIL import Image
from pydantic import BaseModel
from visualime.explain import explain_classification, render_explanation
from xaidemo.tracing import traced

from ..config import settings
from ..model.predict import model, preprocess


class Explanation(BaseModel):
    explanation_id: uuid.UUID
    image: bytes


@traced
def explain(image_file: IO[bytes]) -> Explanation:
    image = Image.open(image_file)
    preprocessed_image = preprocess(image)

    explanation = explain_cnn(preprocessed_image, model)

    return Explanation(
        explanation_id=uuid.uuid4(),
        image=convert_explanation(explanation)
    )


@traced
def convert_explanation(explanation: np.ndarray):
    image = Image.fromarray(explanation.astype(np.float32))

    image = image.resize((settings.streetview_image_size, settings.streetview_image_size),
                         Image.Resampling.BICUBIC)
    buffered = io.BytesIO()
    image.save(buffered, format="png")
    encoded_image_string = base64.b64encode(buffered.getvalue())

    return bytes("data:image/png;base64,", encoding="utf-8") + encoded_image_string


@traced
def explain_cnn(image, model_=model):
    segment_mask, segment_weights = explain_classification(image=image,
                                                           segmentation_method="felzenszwalb",
                                                           segmentation_settings={},
                                                           predict_fn=model_.predict,
                                                           num_of_samples=500,
                                                           p=0.9)

    return render_explanation(image, segment_mask, segment_weights, positive="violet", coverage=0.15, opacity=0.5)
