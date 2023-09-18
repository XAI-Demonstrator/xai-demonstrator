import pytest
from country.explainer import explain


def test_that_an_explanation_is_converted(generate_rgb_image):
    image = generate_rgb_image(224, 224) / 255
    base = explain.convert_explanation(image)

    assert type(base) is bytes 