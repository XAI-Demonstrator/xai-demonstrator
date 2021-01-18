from typing import Tuple

import numpy as np
import torch
from captum.attr import LayerIntegratedGradients
from transformers.modeling_bert import BertForSequenceClassification


def attribute_integrated_gradients(text_input_ids,
                                   ref_input_ids,
                                   target: int,
                                   model: BertForSequenceClassification
                                   ) -> Tuple[np.ndarray, float]:
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

    return scores, delta.item()
