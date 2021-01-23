import pytest

from inspection.explainer import explain


@pytest.mark.integration
def test_that_an_explanation_is_generated(generate_image):
    image_size = (200, 200)
    input_img = generate_image(*image_size)

    output_img = explain.explain(input_img)

    assert output_img.size == image_size
