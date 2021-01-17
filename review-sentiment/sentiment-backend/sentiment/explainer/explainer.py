import pathlib
import re
import string
import uuid
from typing import Tuple, List

import numpy as np
import torch
from pydantic import BaseModel
from transformers import BatchEncoding

from .integrated_gradients import attribute_integrated_gradients
from ..model.model import bert, BertManager

PATH = pathlib.Path(__file__).parent

my_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

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

    return torch.tensor([text_input_ids], device=my_device), torch.tensor([ref_input_ids], device=my_device)


def align_text(text: str,
               encoding: BatchEncoding,
               scores: torch.Tensor) -> List[Tuple[str, float]]:
    split_text = re.findall(r"[\w']+|" + f"[{string.punctuation}]", text)

    words = np.array(encoding.words())
    scores = scores.cpu().detach().numpy()

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
            bert_: BertManager = bert) -> Explanation:
    encoding = bert_.tokenizer.encode_plus(text, add_special_tokens=False)

    text_input_ids, ref_input_ids = construct_input_and_reference(encoding, ref_token_id=bert_.tokenizer.pad_token_id)

    attributions, delta = EXPLAINERS[explainer](text_input_ids, ref_input_ids, target, bert_.model)
    scores = attributions.sum(dim=-1).squeeze(0)

    explanation = filter_attributions(align_text(text=text, encoding=encoding, scores=scores))

    return Explanation(explanation_id=uuid.uuid4(),
                       explanation=explanation,
                       delta=delta.item())
