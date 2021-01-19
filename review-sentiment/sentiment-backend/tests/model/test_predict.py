import uuid

import numpy as np
import pytest

from sentiment.model.predict import predict, Prediction


@pytest.mark.integration
def test_that_predictions_are_returned():
    prediction = predict("The food was excellent!")

    assert len(prediction.prediction) == 5
    assert np.argmax(prediction.prediction) == 4


def test_that_prediction_enforces_correct_length():
    good_prediction = Prediction(prediction_id=uuid.uuid4(),
                                 prediction=[0.2, 0.4, 0.2, 0.15, 0.05])

    with pytest.raises(ValueError):
        bad_prediction = Prediction(prediction_id=uuid.uuid4(),
                                    prediction=[0.2, 0.4, 0.2, 0.2])


def test_that_prediction_sums_to_one():
    good_prediction = Prediction(prediction_id=uuid.uuid4(),
                                 prediction=[0.2, 0.4, 0.2, 0.15, 0.05])

    with pytest.raises(ValueError):
        bad_prediction = Prediction(prediction_id=uuid.uuid4(),
                                    prediction=[0.2, 0.4, 0.2, 0.2, 0.5])

