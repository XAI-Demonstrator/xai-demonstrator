import base64
import io
import uuid
from typing import Any, Dict, IO, Tuple, Union, Optional

import numpy as np
from PIL import Image
from fastapi import HTTPException
from pydantic import BaseModel
from xaidemo.tracing import add_span_attributes, traced

from .explainers.lime_ import lime_explanation
from ..model.model import get_model, default_model
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
            settings: Union[None, Dict[str, Any]] = None,
            model_id: Optional[str] = None) -> Explanation:
    settings = settings or {}

    if model_id is not None:
        try:
            model = get_model(model_id)
        except KeyError as e:
            raise HTTPException(status_code=404, detail=str(e))
    else:
        model = default_model

    explanation_id = uuid.uuid4()

    add_span_attributes({"explanation.id": str(explanation_id), "explanation.method": method})

    input_image = Image.open(image_file)
    explainer_input = preprocess(input_image)[0]

    raw_image = EXPLAINERS[method](explainer_input, model, **settings)

    return Explanation(explanation_id=explanation_id,
                       image=generate_output_image(raw_image, input_image.size))
