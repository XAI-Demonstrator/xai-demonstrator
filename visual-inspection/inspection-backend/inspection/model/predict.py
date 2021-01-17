import uuid

from pydantic import BaseModel
import tensorflow as tf


class Prediction(BaseModel):
    prediction_id: uuid.UUID
    class_id: int



def predict(image: str,
            model: tf.keras.Model) -> Prediction:


    return Prediction(prediction_id=uuid.uuid4(),
                      class_id=0)
