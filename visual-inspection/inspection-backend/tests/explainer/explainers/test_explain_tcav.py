import base64
import io

import pytest
from PIL import Image
from inspection.config import settings
from inspection.explainer import explain


@pytest.mark.integration
def test_tcav_explanation_roundtrip(generate_image):
    image_size = (200, 200)
    input_img = generate_image(*image_size)

    tcav_settings = {
        "explainer": {
            "bottleneck_layer": "global_average_pooling2d_1",
            "cav_dir": "inspection/explainer/explainers/tcav/cavs",
            "cav_manifest_filename": "cav_manifest.json",
        },
        "renderer": {
            "top_k_concepts": 1,
        },
    }

    response = explain.explain(
        input_img,
        model_id=settings.default_model,
        method="tcav",
        settings=tcav_settings,
    )
    output_img_bytes = response.image

    assert output_img_bytes[:22] == bytes("data:image/png;base64,", encoding="utf-8")

    img_data = base64.b64decode(output_img_bytes[22:])
    output_img = Image.open(io.BytesIO(img_data))

    assert output_img.size == image_size
    assert isinstance(response.explanation_str, str)
    assert response.explanation_str
    assert isinstance(response.explanation_strs, dict)
    assert response.explanation_strs["de"]
    assert response.explanation_strs["en"]
