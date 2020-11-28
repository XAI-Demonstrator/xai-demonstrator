import string
import uuid
from typing import Tuple, List

import torch
from captum.attr import LayerIntegratedGradients
from pydantic import BaseModel

from ..model.model import model, sentiment_forward, tokenizer, Prediction

lig = LayerIntegratedGradients(sentiment_forward, model.bert.embeddings)


class Explanation(BaseModel):
    explanation_id: uuid.UUID
    explanation: List[Tuple[str, float]]
    delta: float


def construct_input_and_reference(text: str, ref_token_id):
    text_input_ids = tokenizer.encode(text, add_special_tokens=False)
    ref_input_ids = [ref_token_id] * len(text_input_ids)

    return torch.tensor([text_input_ids]), torch.tensor([ref_input_ids])


def merge_and_attribute(tokens: torch.Tensor, scores: torch.Tensor) -> List[Tuple[str, float]]:
    decoded = [tokenizer.decode([token]) for token in tokens]

    real_words = []
    real_attributions = []

    stack = []

    for i, (token, score) in enumerate(zip(tokens, scores)):
        stack.append((token, score.item()))

        try:
            if decoded[i + 1][:2] == "##":
                continue
        except IndexError:
            pass

        all_tokens, all_scores = tuple(zip(*stack))

        real_words.append(tokenizer.decode(all_tokens))
        real_attributions.append(sum(all_scores) / len(all_scores))

        stack = []

    real_attributions = torch.tensor(real_attributions)
    real_attributions = real_attributions / torch.norm(real_attributions)

    return [(word, score) for word, score in zip(real_words, real_attributions.tolist())
            if word not in string.punctuation]


def explain(text: str) -> Tuple[Prediction, Explanation]:
    # FIXME: Deal with the case of empty text as input
    text_input_ids, ref_input_ids = construct_input_and_reference(text, ref_token_id=tokenizer.pad_token_id)

    prediction = sentiment_forward(text_input_ids)
    target = prediction.argmax().item()

    attributions, delta = lig.attribute(inputs=text_input_ids,
                                        target=4,
                                        baselines=ref_input_ids,
                                        return_convergence_delta=True)

    scores = attributions.sum(dim=-1).squeeze(0)

    explanation = merge_and_attribute(tokens=text_input_ids[0], scores=scores)

    return (Prediction(prediction_id=uuid.uuid4(),
                       prediction=list(map(float, prediction.tolist()[0]))),
            Explanation(explanation_id=uuid.uuid4(),
                        explanation=explanation,
                        delta=delta.item()))
