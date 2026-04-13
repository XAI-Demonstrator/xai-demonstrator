import logging

import numpy as np
import tensorflow as tf
from xaidemo.tracing import traced

from .tcav.tcav_loading import load_cavs_for_config
from .tcav.tcav_models import CAVLoadEntry, TCAVConfiguration, TCAVExplainerConfiguration, TCAVRendererConfiguration
from .tcav.tcav_render import deprocess_mobilenet_v2_image, render_tcav_overlay
from .tcav.tcav_scoring import compute_concept_scores, rank_concept_scores


LOGGER = logging.getLogger(__name__)

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
    **settings: object,
) -> np.ndarray:
    config = TCAVConfiguration(**settings)
    cavs = load_cavs_for_config(config.explainer)

    bottleneck_layer = config.explainer.bottleneck_layer
    try:
        bottleneck_output = model_.get_layer(bottleneck_layer).output
    except ValueError as exc:
        raise ValueError(f"Configured bottleneck layer '{bottleneck_layer}' not found in model.") from exc

    bottleneck_model = tf.keras.Model(inputs=model_.inputs, outputs=bottleneck_output)

    acts = bottleneck_model.predict(input_img[np.newaxis, ...], verbose=0)
    acts_flat = acts.reshape(-1)

    concept_scores = compute_concept_scores(acts_flat, cavs)
    if not concept_scores:
        LOGGER.warning("[TCAV] No concept scores computed.")
        return deprocess_mobilenet_v2_image(input_img)

    ranked_all = rank_concept_scores(concept_scores, by_absolute_value=True)
    k = max(1, config.renderer.top_k_concepts)
    top = ranked_all[:k]

    LOGGER.info("[TCAV] Concept scores (top-k): %s", top)
    LOGGER.debug("[TCAV] Concept scores (all): %s", ranked_all)

    if config.renderer.return_heatmap:
        return render_tcav_overlay(input_img, top, top_k=k)
    return deprocess_mobilenet_v2_image(input_img)
