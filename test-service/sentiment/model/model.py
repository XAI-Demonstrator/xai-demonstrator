import os
import pathlib
from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

PATH = pathlib.Path(__file__).parent


# TODO: Ideally, this should not be done here...
if "CI" in os.environ:
    # Do not load the huge model when testing

    def tokenizer(text, **kwargs) -> dict:
        return {"input": [1, 2, 3]}

    def model(**kwargs) -> torch.tensor:
        return [torch.tensor([[0.99, 0.01]])]

else:
    tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                              cache_dir=PATH/"cache")

    model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                                               cache_dir=PATH/"cache")


def predict_sentiment(text: str) -> List[float]:
    model_input = tokenizer(text, return_tensors="pt")
    model_output = model(**model_input)[0]
    return list(map(float, torch.softmax(model_output, dim=1).tolist()[0]))
