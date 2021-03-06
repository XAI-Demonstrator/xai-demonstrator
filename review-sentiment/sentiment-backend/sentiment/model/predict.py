import math
import uuid
from typing import List

import torch
from pydantic import BaseModel, validator
from xaidemo.tracing import add_span_attributes, traced

from .model import BertManager, bert

my_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class Prediction(BaseModel):
    prediction_id: uuid.UUID
    prediction: List[float]

    @validator('prediction')
    def prediction_must_be_of_length_five(cls, v):
        if len(v) != 5:
            raise ValueError(f"Prediction must be list of length 5 (actual: {len(v)}).")
        return v

    @validator('prediction')
    def prediction_must_sum_to_one(cls, v):
        if not math.isclose(sum(v), 1.0, abs_tol=1e-6):
            raise ValueError(f"Prediction must sum to 1.0 (actual: {sum(v)}).")
        return v


@traced(attributes={"torch.device": str(my_device), "torch.device.type": my_device.type})
def predict(text: str,
            bert_: BertManager = bert) -> Prediction:
    prediction_id = uuid.uuid4()

    tokens = bert_.tokenizer.encode(text, add_special_tokens=False)

    add_span_attributes({
        "prediction.id": str(prediction_id),
        "text.chars": len(text),
        "text.tokens": len(tokens)
    })

    model_input = torch.tensor([tokens], dtype=torch.int64, device=my_device)
    model_output = bert_.model(model_input)
    prediction = torch.softmax(model_output[0], dim=1)

    return Prediction(prediction_id=prediction_id,
                      prediction=list(map(float, prediction[0].tolist())))
