from typing import Tuple

import numpy as np


# noinspection PyUnusedLocal
def attribute_random_words(text_input_ids, **kwargs) -> Tuple[np.ndarray, None]:
    num_of_tokens = len(text_input_ids)

    alpha = np.ones(num_of_tokens)
    raw_scores = np.random.default_rng().dirichlet(alpha, 1)[0]

    scores = np.where(np.random.default_rng().random(num_of_tokens) > 0.5,
                      raw_scores, -raw_scores)

    return scores, None
