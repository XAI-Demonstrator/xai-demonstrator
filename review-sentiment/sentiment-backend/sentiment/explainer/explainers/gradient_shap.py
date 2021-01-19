from typing import Tuple, Dict

import numpy as np
import torch
from captum.attr import LayerGradientShap
from transformers.modeling_bert import BertForSequenceClassification


# noinspection PyUnusedLocal
def attribute_gradient_shap(text_input_ids: torch.Tensor,
                            ref_input_ids: torch.Tensor,
                            target: int,
                            model: BertForSequenceClassification,
                            **kwargs) -> Tuple[np.ndarray, Dict[str, float]]:

    # TODO: We need to start attribution at the input of the layer after the embedding
    #       because LGS uses a Gaussian distribution to disturb the layer's input:
    #       (1) Calculate the embedding outputs for input and ref
    #       (2) Create a new model that goes from "after embedding" to "output"

    def forward(model_input):
        pred = model(model_input)
        return torch.softmax(pred[0], dim=1)

    lgs = LayerGradientShap(forward,
                            model.bert.embeddings)

    attributions, delta = lgs.attribute(inputs=text_input_ids,
                                        target=target,
                                        baselines=ref_input_ids,
                                        return_convergence_delta=True,
                                        attribute_to_layer_input=True)

    scores = attributions.sum(dim=-1).squeeze(0)
    scores = scores.cpu().detach().numpy()

    return scores, {"delta": delta.item()}
