import pathlib
import re
import string
import uuid
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
from pydantic import BaseModel

from .explainers.integrated_gradients import attribute_integrated_gradients
from .explainers.random_words import attribute_random_words
from .explainers.shapley_value_sampling import attribute_sampled_shapley_values
from ..model.model import BertManager, bert

PATH = pathlib.Path(__file__).parent

my_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

with open(PATH / "small_words_to_filter.txt", "rt", encoding="utf-8") as f:
    STOPWORDS = [word.strip() for word in f]

EXPLAINERS = {
    "integrated_gradients": attribute_integrated_gradients,
    "random": attribute_random_words,
    "shapley_value_sampling": attribute_sampled_shapley_values
}


class Explanation(BaseModel):
    explanation_id: uuid.UUID
    explanation: List[Tuple[str, float]]
    meta: Optional[Dict[str, Any]]


def construct_input_and_reference(text_input_ids: List[int],
                                  ref_token_id: int) -> Tuple[torch.Tensor, torch.Tensor]:
    ref_input_ids = [ref_token_id] * len(text_input_ids)

    return torch.tensor([text_input_ids], device=my_device), torch.tensor([ref_input_ids], device=my_device)


def align_text(text: str,
               words: np.ndarray,
               scores: np.ndarray) -> List[Tuple[str, float]]:
    split_text = re.findall(r"[\w']+|" + f"[{string.punctuation}]", text)

    return [(word, float(np.mean(scores[words == idx])))
            for idx, word in enumerate(split_text)]


def filter_attributions(attributions: List[Tuple[str, float]],
                        remove_stopwords: bool = True,
                        remove_punctuation: bool = True) -> List[Tuple[str, float]]:
    if remove_punctuation:
        attributions = ((word, score if word not in string.punctuation else 0.0)
                        for word, score in attributions)

    if remove_stopwords:
        attributions = ((word, score if word.lower() not in STOPWORDS else 0.0)
                        for word, score in attributions)

    return list(attributions)


def explain(text: str, target: int,
            explainer: str = "integrated_gradients",
            settings: Optional[Dict[str, Any]] = None,
            bert_: BertManager = bert) -> Explanation:
    settings = settings or {}

    encoding = bert_.tokenizer.encode_plus(text, add_special_tokens=False)

    text_input_ids, ref_input_ids = construct_input_and_reference(encoding["input_ids"],
                                                                  ref_token_id=bert_.tokenizer.pad_token_id)

    scores, meta = EXPLAINERS[explainer](
        text_input_ids=text_input_ids,
        ref_input_ids=ref_input_ids,
        target=target,
        model=bert_.model,
        settings=settings)

    explanation = filter_attributions(align_text(text=text,
                                                 words=np.array(encoding.words()),
                                                 scores=scores))

    return Explanation(explanation_id=uuid.uuid4(),
                       explanation=explanation,
                       meta=meta)
