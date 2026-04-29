import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import tensorflow as tf
from pydantic import BaseModel, Field
from xaidemo.tracing import traced

from .tcav.tcav_loading import load_cavs_for_config
from .tcav.tcav_models import TCAVConfiguration, TCAVExplainerConfiguration, TCAVRendererConfiguration
from .tcav.tcav_scoring import compute_concept_scores, rank_concept_scores

LOGGER = logging.getLogger(__name__)

__all__ = [
    "TCAVConceptScore",
    "TCAVAnalysis",
    "TCAVConfiguration",
    "TCAVExplainerConfiguration",
    "TCAVRendererConfiguration",
    "compute_tcav_analysis",
    "tcav_explanation",
    "build_tcav_explanation_sentence",
    "humanize_tcav_concept",
]

_LABELS_PATH = Path(__file__).parent / "tcav" / "tcav_concept_labels_de.json"


def _load_concept_labels() -> dict[str, str]:
    try:
        return json.loads(_LABELS_PATH.read_text(encoding="utf-8"))
    except OSError:
        return {}


_CONCEPT_LABELS = _load_concept_labels()


class TCAVConceptScore(BaseModel):
    concept: str
    score: float


class TCAVAnalysis(BaseModel):
    concept_scores: Dict[str, float] = Field(default_factory=dict)
    ranked_concept_scores: List[TCAVConceptScore] = Field(default_factory=list)


def _humanize_tcav_concept(concept: str) -> str:
    mapped = _CONCEPT_LABELS.get(concept)
    if mapped:
        return mapped
    fallback = concept.rsplit("/", 1)[-1].replace("_", " ").strip()
    return fallback or concept


def humanize_tcav_concept(concept: str) -> str:
    return _humanize_tcav_concept(concept)


def _describe_score_strength(score: float) -> str:
    abs_score = abs(score)
    if abs_score >= 0.25:
        return "stark"
    if abs_score >= 0.15:
        return "mittel"
    return "schwach"


def _describe_score_direction(score: float) -> str:
    return "unterstützt" if score >= 0 else "spricht gegen"


def build_tcav_explanation_sentence(analysis: TCAVAnalysis, top_k: int = 3) -> str:
    ranked = list(analysis.ranked_concept_scores)[: max(1, top_k)]
    if not ranked:
        return "Ich kann kein klares Konzept erkennen, das diese Vorhersage erklärt."

    prefixes = ("Am wichtigsten ist", "Danach kommt", "Als drittes folgt")
    sentences = []

    for index, item in enumerate(ranked[:3]):
        prefix = prefixes[index] if index < len(prefixes) else "Ausserdem gibt es"
        sentences.append(
            f"{prefix} '{_humanize_tcav_concept(item.concept)}'. "
            f"Es {_describe_score_direction(item.score)} die Vorhersage ({_describe_score_strength(item.score)})."
        )

    return " ".join(sentences)


def compute_tcav_analysis(input_img: np.ndarray, model_: tf.keras.models.Model, **settings: object) -> TCAVAnalysis:
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
    ranked_all = rank_concept_scores(concept_scores, by_absolute_value=True)
    return TCAVAnalysis(
        concept_scores=concept_scores,
        ranked_concept_scores=[TCAVConceptScore(concept=concept, score=score) for concept, score in ranked_all],
    )


@traced(label="compute_explanation", attributes={"explanation.method": "tcav"})
def tcav_explanation(
        input_img: np.ndarray,
        model_: tf.keras.models.Model,
        analysis: Optional[TCAVAnalysis] = None,
        **settings: object,
) -> np.ndarray:
    config = TCAVConfiguration(**settings)
    analysis = analysis or compute_tcav_analysis(input_img, model_, **settings)

    if not analysis.concept_scores:
        LOGGER.warning("[TCAV] No concept scores computed.")
        return _deprocess_mobilenet_v2_image(input_img)

    k = max(1, config.renderer.top_k_concepts)
    top_concepts = analysis.ranked_concept_scores[:k]
    LOGGER.info("[TCAV] Concept scores (top-k): %s", [(c.concept, c.score) for c in top_concepts])

    return _deprocess_mobilenet_v2_image(input_img)


def _deprocess_mobilenet_v2_image(input_img: np.ndarray) -> np.ndarray:
    restored = (input_img + 1.0) / 2.0
    return np.clip(restored, 0.0, 1.0).astype(np.float32)
