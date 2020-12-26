import string
import uuid
from typing import Tuple, List

import torch
import re
import numpy as np
import pathlib

from pydantic import BaseModel
from transformers import BatchEncoding
from transformers.tokenization_bert import BertTokenizer
from transformers.modeling_bert import BertForSequenceClassification

from .integrated_gradients import attribute_integrated_gradients
from ..model.model import get

PATH = pathlib.Path(__file__).parent

with open(PATH/"small_words_to_filter.txt", "rt", encoding="utf-8") as f:
    STOPWORDS = [word.strip() for word in f]

EXPLAINERS = {
    "integrated_gradients": attribute_integrated_gradients
}


class Explanation(BaseModel):
    explanation_id: uuid.UUID
    explanation: List[Tuple[str, float]]
    delta: float


class Explainer:

    def attribute(self, text_input_ids, ref_input_ids, target):
        raise NotImplementedError


def construct_input_and_reference(encoding: BatchEncoding,
                                  ref_token_id: int):

    text_input_ids = encoding["input_ids"]
    ref_input_ids = [ref_token_id] * len(text_input_ids)

    return torch.tensor([text_input_ids]), torch.tensor([ref_input_ids])


def align_text(text: str,
               encoding: BatchEncoding,
               scores: torch.Tensor) -> List[Tuple[str, float]]:
    split_text = re.findall(r"[\w']+|" + f"[{string.punctuation}]", text)

    words = np.array(encoding.words())
    scores = scores.detach().numpy()

    return [(word, float(np.mean(scores[words == idx])))
            for idx, word in enumerate(split_text)]


def filter_attributions(attributions, remove_stopwords=True, remove_punctuation=True):
    if remove_punctuation:
        attributions = ((word, score if word not in string.punctuation else 0.0) for word, score in attributions)

    if remove_stopwords:
        attributions = ((word, score if word not in STOPWORDS else 0.0) for word, score in attributions)

    return list(attributions)


def explain(text: str, target: int,
            explainer: str = "integrated_gradients",
            model: BertForSequenceClassification = get.model,
            tokenizer: BertTokenizer = get.tokenizer) -> Explanation:
    encoding = tokenizer.encode_plus(text, add_special_tokens=False)

    text_input_ids, ref_input_ids = construct_input_and_reference(encoding, ref_token_id=tokenizer.pad_token_id)

    attributions, delta = EXPLAINERS[explainer](text_input_ids, ref_input_ids, target, model)
    scores = attributions.sum(dim=-1).squeeze(0)

    explanation = filter_attributions(align_text(text=text, encoding=encoding, scores=scores))

    return Explanation(explanation_id=uuid.uuid4(),
                       explanation=explanation,
                       delta=delta.item())
