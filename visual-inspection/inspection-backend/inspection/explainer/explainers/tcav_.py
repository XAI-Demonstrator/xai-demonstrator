from typing import Dict

import numpy as np
import tensorflow as tf
from xaidemo.tracing import traced

from .tcav.tcav_loading import load_cavs_for_config
from .tcav.tcav_models import CAVLoadEntry, TCAVConfiguration, TCAVExplainerConfiguration, TCAVRendererConfiguration
from .tcav.tcav_scoring import compute_concept_scores, rank_concept_scores

__all__ = [
    "CAVLoadEntry",
    "TCAVConfiguration",
    "TCAVExplainerConfiguration",
    "TCAVRendererConfiguration",
    "tcav_explanation",
]


@traced(label="compute_explanation", attributes={"explanation.method": "tcav"})
def tcav_explanation(
    input_img: np.ndarray,
    model_: tf.keras.models.Model,
    **settings: Dict[str, object],
) -> np.ndarray:
    """Compute TCAV concept scores for a single input image."""
    config = TCAVConfiguration(**settings)
    cavs = load_cavs_for_config(config.explainer)

    bottleneck_layer = config.explainer.bottleneck_layer
    bottleneck_output = model_.get_layer(bottleneck_layer).output
    bottleneck_model = tf.keras.Model(inputs=model_.inputs, outputs=bottleneck_output)

    acts = bottleneck_model.predict(input_img[np.newaxis, ...], verbose=0)
    acts_flat = acts.reshape(-1)

    concept_scores = compute_concept_scores(acts_flat, cavs)
    if not concept_scores:
        print("[TCAV] WARNING: No concept scores computed.")
        return input_img

    ranked_all = rank_concept_scores(concept_scores, by_absolute_value=True)
    k = max(1, config.renderer.top_k_concepts)
    top = ranked_all[:k]

    print("[TCAV] Concept scores (top-k):", top)
    print("[TCAV] Concept scores (all):", ranked_all)

    return input_img
