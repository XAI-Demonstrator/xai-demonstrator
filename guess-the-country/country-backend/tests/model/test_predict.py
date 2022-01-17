import pytest
import pathlib
from country.model import predict



def test_that_standard_images_are_preprocessed(generate_image):
    img = generate_image(448, 448)

    result = predict.preprocess(img)

    assert result.shape == (1, 224, 224, 3)


# def test_that_a_prediction_is_generated(generate_image):
#     img = generate_image(224, 224)
#     result = predict.preprocess(img)
#     prediction = predict.predict_image(result)
#     assert type(prediction) is str

def test_that_a_base64_image_is_preprocessed(generate_base64):

    result = predict.load_image(generate_base64())

    assert result.shape == (448, 448, 3)
