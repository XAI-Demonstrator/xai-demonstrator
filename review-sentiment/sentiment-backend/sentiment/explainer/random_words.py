import numpy as np


def attribute_random_words(text_input_ids, **kwargs):
    num_of_tokens = len(text_input_ids)

    alpha = np.ones(num_of_tokens)
    raw_attributions = np.random.default_rng().dirichlet(alpha, 1)[0]

    attributions = np.where(np.random.default_rng().random(num_of_tokens) > 0.5,
                            raw_attributions, -raw_attributions)

    return attributions, 0.0
