import numpy as np
import pytest

from sentiment.model.predict import predict


@pytest.mark.integration
def test_that_predictions_are_returned():

    prediction = predict("The food was excellent!")

    assert len(prediction.prediction) == 5
    assert np.argmax(prediction.prediction) == 4
