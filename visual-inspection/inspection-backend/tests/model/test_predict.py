import pathlib

import pytest
from PIL import Image

from inspection.config import settings
from inspection.model import predict


def test_that_standard_images_are_preprocessed(generate_image):
    img = generate_image(224, 224)
    input_img = Image.open(img)

    result = predict.preprocess(input_img)

    assert result.shape == (1, 224, 224, 3)


def test_that_standard_images_with_alpha_channel_are_preprocessed(generate_image):
    img = generate_image(224, 224, alpha=True)
    input_img = Image.open(img)

    result = predict.preprocess(input_img)

    assert result.shape == (1, 224, 224, 3)


def test_that_non_square_images_are_preprocessed(generate_image):
    img = generate_image(100, 443)
    input_img = Image.open(img)

    result = predict.preprocess(input_img)

    assert result.shape == (1, 224, 224, 3)


@pytest.mark.integration
def test_that_a_prediction_is_generated(generate_image):
    img = generate_image(224, 224)

    _ = predict.predict(img, model_id=settings.default_model)


def test_that_input_is_saved(generate_image, mocker, tmp_path):
    predict.settings.log_path = tmp_path
    mocker.patch.object(predict, "predict_class", return_value=("myclass", 0.8))
    mocker.patch.object(predict, "get_model", return_value=None)

    img = generate_image(112, 112)

    predict.settings.log_input = True
    prediction = predict.predict(img, model_id="my_model")
    expected_path = tmp_path / f"{str(prediction.prediction_id)}.png"
    assert pathlib.Path.exists(expected_path)

    predict.settings.log_input = False
    prediction = predict.predict(img, model_id="my_model")
    expected_path = tmp_path / f"{str(prediction.prediction_id)}.png"
    assert not pathlib.Path.exists(expected_path)
