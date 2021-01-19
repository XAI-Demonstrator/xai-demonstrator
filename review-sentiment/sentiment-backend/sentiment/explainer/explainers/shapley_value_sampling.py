from typing import Any, Dict, Tuple

import numpy as np
import torch
from captum.attr import ShapleyValueSampling
from transformers import BertForSequenceClassification


# noinspection PyUnusedLocal
def attribute_sampled_shapley_values(text_input_ids: torch.Tensor,
                                     target: int,
                                     model: BertForSequenceClassification,
                                     settings: Dict[str, Any],
                                     **kwargs) -> Tuple[np.ndarray, None]:
    def forward(model_input):
        pred = model(model_input)
        return torch.softmax(pred[0], dim=1)

    svs = ShapleyValueSampling(forward)

    attributions = svs.attribute(inputs=text_input_ids,
                                 target=target,
                                 n_samples=settings.get("n_samples", 25))

    scores = attributions.cpu().detach().numpy().flatten()

    return scores, None
