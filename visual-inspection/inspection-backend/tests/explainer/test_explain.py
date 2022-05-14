import base64
import io

import pytest
from PIL import Image

from inspection.config import settings
from inspection.explainer import explain


@pytest.mark.integration
def test_that_an_explanation_is_generated(generate_image):
    image_size = (200, 200)
    input_img = generate_image(*image_size)

    output_img_bytes = explain.explain(input_img,
                                       model_id=settings.default_model,
                                       method=settings.default_explainer).image
    img_data = base64.b64decode(output_img_bytes[22:])
    output_img = Image.open(io.BytesIO(img_data))

    assert output_img_bytes[:22] == bytes("data:image/png;base64,", encoding='utf-8')
    assert output_img.size == image_size
