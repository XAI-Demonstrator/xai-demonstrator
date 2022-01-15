import pytest
import pathlib

from country.model import predict
from PIL import Image


def test_that_standard_images_are_preprocessed(generate_image):
    img = generate_image(448, 448)
    input_img = Image.open(img)

    result = predict.preprocess(input_img)

    assert result.shape == (1, 224, 224, 3)


@pytest.mark.integration
def test_that_a_prediction_is_generated(generate_image):
    img = generate_image(224, 224)

    _ = predict.predict_image(img)

@pytest.mark.integration
def test_that_a_base64_image_is_preprocessed(gernerate_base64):
    img = gernerate_base64(448, 448)

    result = load_image(img)

    assert result.shape == (1, 448, 448, 3)

