import base64
import io
import uuid
from typing import Any, Dict, IO, Tuple, Union

import numpy as np
import tensorflow as tf
from PIL import Image
from pydantic import BaseModel
from xaidemo.tracing import add_span_attributes, traced

from .explainers.lime_ import lime_explanation
from ..model.model import model
from ..model.predict import preprocess

EXPLAINERS = {
    "lime": lime_explanation
}


@traced
def generate_output_image(raw_image: np.ndarray,
                          size: Tuple[int, int]) -> bytes:
    exp_image = Image.fromarray((255 * raw_image).astype(np.uint8))
    exp_image = exp_image.resize(size, Image.BICUBIC)

    buffered = io.BytesIO()
    exp_image.save(buffered, format="png")
    encoded_image_string = base64.b64encode(buffered.getvalue())
    return bytes("data:image/png;base64,", encoding="utf-8") + encoded_image_string


class Explanation(BaseModel):
    explanation_id: uuid.UUID
    image: bytes


@traced
def explain(image_file: IO[bytes],
            method: str,
            index_of_label_to_explain: int,
            positive_only_parameter: bool,
            settings: Union[None, Dict[str, Any]] = None,
            model_: tf.keras.models.Model = model) -> Explanation:
    settings = settings or {}
    explanation_id = uuid.uuid4()

    add_span_attributes({"explanation.id": str(explanation_id), "explanation.method": method})

    input_image = Image.open(image_file)
    explainer_input = preprocess(input_image)[0]

    raw_image = EXPLAINERS[method](explainer_input, model_, index_of_label_to_explain,positive_only_parameter, **settings)
    return Explanation(explanation_id=explanation_id,
                       image=generate_output_image(raw_image, input_image.size))
