import pytest

from inspection.model import predict


def test_that_standard_images_are_preprocessed(generate_image):
    img = generate_image(224, 224)

    result = predict.preprocess(img)

    assert result.shape == (1, 224, 224, 3)


def test_that_standard_images_with_alpha_channel_are_preprocessed(generate_image):
    img = generate_image(224, 224, alpha=True)

    result = predict.preprocess(img)

    assert result.shape == (1, 224, 224, 3)


def test_that_non_square_images_are_preprocessed(generate_image):
    img = generate_image(100, 443)

    result = predict.preprocess(img)

    assert result.shape == (1, 224, 224, 3)


@pytest.mark.integration
def test_that_a_prediction_is_generated(generate_image):
    img = generate_image(224, 224)

    _ = predict.predict(img)
