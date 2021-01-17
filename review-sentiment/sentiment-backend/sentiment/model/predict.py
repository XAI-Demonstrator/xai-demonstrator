import uuid
from typing import List

import torch
from pydantic import BaseModel, validator

from .model import bert, BertManager

my_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class Prediction(BaseModel):
    prediction_id: uuid.UUID
    prediction: List[float]

    @validator('prediction')
    def prediction_must_be_of_length_five(cls, v):
        if len(v) != 5:
            raise ValueError("Prediction must be list of length 5.")
        return v


def predict(text: str,
            bert_: BertManager = bert) -> Prediction:
    model_input = torch.tensor([bert_.tokenizer.encode(text, add_special_tokens=False)],
                               dtype=torch.int64, device=my_device)
    model_output = bert_.model(model_input)
    prediction = torch.softmax(model_output[0], dim=1)

    return Prediction(prediction_id=uuid.uuid4(),
                      prediction=list(map(float, prediction[0].tolist())))
