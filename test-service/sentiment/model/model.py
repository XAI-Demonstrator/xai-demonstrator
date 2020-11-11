from typing import Callable
import pathlib
import uuid
from typing import List

import torch
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

PATH = pathlib.Path(__file__).parent


class LazyLoader:
    """Prevent huge assets from being loaded at startup, allows for mocking."""

    def __init__(self):
        self._object = None

    def load(self) -> Callable:
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        if self._object is None:
            self._object = self.load()

        return self._object(*args, **kwargs)


class Model(LazyLoader):

    def load(self):
        return AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                                                  cache_dir=PATH / "cache")

    @property
    def bert(self):
        if self._object is None:
            self._object = self.load()
        return self._object.bert


class Tokenizer(LazyLoader):

    def load(self):
        return AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                             cache_dir=PATH / "cache")

    def encode(self, *args, **kwargs):
        if self._object is None:
            self._object = self.load()
        return self._object.encode(*args, **kwargs)

    @property
    def pad_token_id(self):
        if self._object is None:
            self._object = self.load()
        return self._object.pad_token_id


model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                                           cache_dir=PATH / "cache")
tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                          cache_dir=PATH / "cache")


class Prediction(BaseModel):
    prediction_id: uuid.UUID
    prediction: List[float]


def sentiment_forward(model_input):
    pred = model(model_input)
    return torch.softmax(pred[0], dim=1)


def predict_sentiment(text: str) -> Prediction:
    # TODO: Empty texts cause all sorts of issues, no need to call the model
    #       This workaround is likely to cause issues in the frontend, though
    if not text:
        return Prediction(prediction_id=uuid.uuid4(), prediction=[0.0] * 5)

    model_input = torch.tensor([tokenizer.encode(text, add_special_tokens=False)], dtype=torch.int64)
    model_output = sentiment_forward(model_input)
    return Prediction(prediction_id=uuid.uuid4(),
                      prediction=list(map(float, model_output.tolist()[0])))
