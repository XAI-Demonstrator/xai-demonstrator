import numpy as np
import pytest
from PIL import Image

from country.model import predict


@pytest.mark.integration
def test_that_a_city_is_predicted(generate_png_image):
    img = generate_png_image(448, 448)
    _ = predict.predict_city(img)


def test_that_images_are_preprocessed(generate_rgb_image):
    img = Image.fromarray(generate_rgb_image(448, 448))

    result = predict.preprocess(img)
    in_range = (np.where(np.logical_and(result >= -1, result <= 1), 1, 0)).reshape(-1, )  # 1 if in [-1, 1] 0 otherwise

    assert result.shape == (1, 224, 224, 3)
    assert sum(in_range) == len(in_range)
