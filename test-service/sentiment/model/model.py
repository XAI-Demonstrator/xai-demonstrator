from typing import List
import pathlib

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


PATH = pathlib.Path(__file__).parent

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                          cache_dir=PATH/"cache")

model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                                           cache_dir=PATH/"cache")


def predict_sentiment(text: str) -> List[float]:
    model_input = tokenizer(text, return_tensors="pt")
    model_output = model(**model_input)[0]
    return list(map(float, torch.softmax(model_output, dim=1).tolist()[0]))
