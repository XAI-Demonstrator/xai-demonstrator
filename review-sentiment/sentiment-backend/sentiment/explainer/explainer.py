import pathlib
import re
import string
import threading
import uuid
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
from pydantic import BaseModel
from xaidemo.tracing import add_span_attributes, traced

from .explainers.gradient_shap import attribute_gradient_shap
from .explainers.integrated_gradients import attribute_integrated_gradients
from .explainers.random_words import attribute_random_words
from .explainers.shapley_value_sampling import attribute_sampled_shapley_values
from ..model.model import BertManager, bert

PATH = pathlib.Path(__file__).parent

my_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

explanation_lock = threading.Lock()

with open(PATH / "small_words_to_filter.txt", "rt", encoding="utf-8") as f:
    STOPWORDS = [word.strip() for word in f]

EXPLAINERS = {
    "gradient_shap": attribute_gradient_shap,
    "integrated_gradients": attribute_integrated_gradients,
    "random_words": attribute_random_words,
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
               word_ids: np.ndarray,
               scores: np.ndarray) -> List[Tuple[str, float]]:
    split_text = re.findall(r"[\w']+|" + f"[{string.punctuation}]", text)

    return [(word, float(np.mean(scores[word_ids == idx])))
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


@traced(attributes={"torch.device": str(my_device), "torch.device.type": my_device.type})
def explain(text: str,
            target: int,
            explainer: str,
            settings: Optional[Dict[str, Any]] = None,
            bert_: BertManager = bert) -> Explanation:
    settings = settings or {}
    tokenizer = bert_.tokenizer

    explanation_id = uuid.uuid4()

    encoded_text = tokenizer.encode_plus(text, add_special_tokens=False)

    add_span_attributes({
        "explanation.id": str(explanation_id),
        "explanation.method": explainer,
        "text.chars": len(text),
        "text.tokens": len(encoded_text["input_ids"])
    })

    text_input_ids, ref_input_ids = construct_input_and_reference(encoded_text["input_ids"],
                                                                  ref_token_id=tokenizer.pad_token_id)

    # Captum explainers (at least integrated_gradients) are apparently not thread-safe
    with explanation_lock:
        scores, meta = EXPLAINERS[explainer](
            text_input_ids=text_input_ids,
            ref_input_ids=ref_input_ids,
            target=target,
            model=bert_.model,
            settings=settings)

    explanation = filter_attributions(align_text(text=text,
                                                 word_ids=np.array(encoded_text.word_ids()),
                                                 scores=scores))

    return Explanation(explanation_id=explanation_id,
                       explanation=explanation,
                       meta=meta)
