from typing import Dict, Tuple

import numpy as np
import torch
from captum.attr import LayerGradientShap
from transformers.models.bert.modeling_bert import BertForSequenceClassification


def create_partial_model(model: BertForSequenceClassification):

    def forward(embedded_input):
        encoder_output = model.bert.encoder(embedded_input)
        pooled = model.bert.pooler(encoder_output[0])
        model_output = model.classifier(pooled)
        return torch.softmax(model_output, dim=1)

    return forward, model.bert.encoder


# noinspection PyUnusedLocal
def attribute_gradient_shap(text_input_ids: torch.Tensor,
                            ref_input_ids: torch.Tensor,
                            target: int,
                            model: BertForSequenceClassification,
                            **kwargs) -> Tuple[np.ndarray, Dict[str, float]]:

    embedded_text_inputs = model.bert.embeddings(text_input_ids)
    embedded_ref_inputs = model.bert.embeddings(ref_input_ids)

    forward, attribution_layer = create_partial_model(model)

    lgs = LayerGradientShap(forward,
                            attribution_layer)

    attributions, delta = lgs.attribute(inputs=embedded_text_inputs,
                                        target=target,
                                        baselines=embedded_ref_inputs,
                                        return_convergence_delta=True,
                                        attribute_to_layer_input=True)

    scores = attributions.sum(dim=-1).squeeze(0)
    scores = scores.cpu().detach().numpy()

    return scores, {"delta": delta.cpu().detach().numpy().tolist()}
