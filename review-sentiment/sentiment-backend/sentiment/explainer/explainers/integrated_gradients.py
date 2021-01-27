from typing import Dict, Tuple

import numpy as np
import torch
from captum.attr import LayerIntegratedGradients
from transformers import BertForSequenceClassification
from xaidemo.tracing import traced


# noinspection PyUnusedLocal
@traced(label="attribute", attributes={"explanation.method": "integrated_gradients"})
def attribute_integrated_gradients(text_input_ids: torch.Tensor,
                                   ref_input_ids: torch.Tensor,
                                   target: int,
                                   model: BertForSequenceClassification,
                                   **kwargs) -> Tuple[np.ndarray, Dict[str, float]]:
    def forward(model_input):
        pred = model(model_input)
        return torch.softmax(pred[0], dim=1)

    # TODO: Investigate whether instantiating the LIG is expensive
    lig = LayerIntegratedGradients(forward,
                                   model.bert.embeddings)

    attributions, delta = lig.attribute(inputs=text_input_ids,
                                        target=target,
                                        baselines=ref_input_ids,
                                        return_convergence_delta=True)

    scores = attributions.sum(dim=-1).squeeze(0)
    scores = scores.cpu().detach().numpy()

    return scores, {"delta": delta.item()}
