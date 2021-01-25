from typing import Tuple

import numpy as np
import torch

from ...tracing import traced


# noinspection PyUnusedLocal
@traced(label="attribute", attributes={"explanation.method": "random_words"})
def attribute_random_words(text_input_ids: torch.Tensor, **kwargs) -> Tuple[np.ndarray, None]:
    num_of_tokens = text_input_ids.shape[1]

    alpha = np.ones(num_of_tokens)
    raw_scores = np.random.default_rng().dirichlet(alpha, 1)[0]

    scores = np.where(np.random.default_rng().random(num_of_tokens) > 0.5,
                      raw_scores, -raw_scores)

    return scores, None
