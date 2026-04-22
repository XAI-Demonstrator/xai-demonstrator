import base64
import io
import uuid
from typing import Any, Dict, IO, Optional, Tuple, Union

import numpy as np
from PIL import Image
from pydantic import BaseModel
from xaidemo.tracing import add_span_attributes, traced

# from .explainers.lime_ import lime_explanation  TODO - JUST FOR TESTING
from .explainers.tcav_ import compute_tcav_analysis, tcav_explanation
from .explainers.tcav_text import build_tcav_explanation_sentence
from ..model.model import get_model
from ..model.predict import preprocess

EXPLAINERS = {
#    "lime": lime_explanation, TODO - JUST FOR TESTING
    "tcav": tcav_explanation
}


@traced
def generate_output_image(raw_image: np.ndarray,
                          size: Tuple[int, int]) -> bytes:
    exp_image = Image.fromarray((255 * raw_image).astype(np.uint8))
    exp_image = exp_image.resize(size, Image.Resampling.BICUBIC)

    buffered = io.BytesIO()
    exp_image.save(buffered, format="png")
    encoded_image_string = base64.b64encode(buffered.getvalue())

    return bytes("data:image/png;base64,", encoding="utf-8") + encoded_image_string



class Explanation(BaseModel):
    explanation_id: uuid.UUID
    image: bytes
    explanation_str: Optional[str] = None


@traced
def explain(image_file: IO[bytes],
            model_id: str,
            method: str,
            settings: Union[None, Dict[str, Any]] = None) -> Explanation:
    settings = settings or {}
    model = get_model(model_id)

    explanation_id = uuid.uuid4()
    add_span_attributes({"explanation.id": str(explanation_id),
                         "explanation.method": method,
                         "explanation.model": model_id})

    input_image = Image.open(image_file)
    explainer_input = preprocess(input_image)[0]

    if method == "tcav":
        analysis = compute_tcav_analysis(explainer_input, model, **settings)
        raw_image = tcav_explanation(explainer_input, model, analysis=analysis, **settings)
        renderer_settings = settings.get("renderer", {})
        top_k = int(renderer_settings.get("top_k_concepts", 3))
        explanation_str = build_tcav_explanation_sentence(analysis, top_k=top_k)

        return Explanation(explanation_id=explanation_id,
                           image=generate_output_image(raw_image, input_image.size),
                           explanation_str=explanation_str)
    else:
        raw_image = EXPLAINERS[method](explainer_input, model, **settings)

        return Explanation(explanation_id=explanation_id,
                           image=generate_output_image(raw_image, input_image.size))
