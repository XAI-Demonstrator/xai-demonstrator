from inspection.model import predict


def test_load_and_preprocessing(dummy_image):
    result = predict.load_and_preprocess(dummy_image)

    assert result.shape == (1, 224, 224, 3)
