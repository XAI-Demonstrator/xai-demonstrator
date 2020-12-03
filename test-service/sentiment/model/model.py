import pathlib
import uuid
from typing import List

import torch
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers.modeling_bert import BertForSequenceClassification
from transformers.tokenization_bert import BertTokenizer

PATH = pathlib.Path(__file__).parent


class ObjectManager:

    def __init__(self):
        self._model = None
        self._tokenizer = None

    @property
    def model(self) -> BertForSequenceClassification:
        if self._model is None:
            self._model = self.load_model()
        return self._model
    
    @property
    def tokenizer(self) -> BertTokenizer:
        if self._tokenizer is None:
            self._tokenizer = self.load_tokenizer()
        return self._tokenizer

    @staticmethod
    def load_model() -> BertForSequenceClassification:
        return AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                                                  cache_dir=PATH / "cache")

    @staticmethod
    def load_tokenizer() -> BertTokenizer:
        return AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                             cache_dir=PATH / "cache")


get = ObjectManager()


class Prediction(BaseModel):
    prediction_id: uuid.UUID
    prediction: List[float]


def sentiment_forward(model_input):
    model = get.model
    pred = model(model_input)
    return torch.softmax(pred[0], dim=1)


def predict_sentiment(text: str) -> Prediction:
    tokenizer = get.tokenizer
    model_input = torch.tensor([tokenizer.encode(text, add_special_tokens=False)], dtype=torch.int64)
    model_output = sentiment_forward(model_input)
    return Prediction(prediction_id=uuid.uuid4(),
                      prediction=list(map(float, model_output.tolist()[0])))
