import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Literal

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
    "build_tcav_explanation_sentences",
    "humanize_tcav_concept",
]

_LABELS_PATHS = {
    "de": Path(__file__).parent / "tcav" / "tcav_concept_labels_de.json",
    "en": Path(__file__).parent / "tcav" / "tcav_concept_labels_en.json",
}


def _load_concept_labels(path: Path) -> dict[str, str]:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig").strip())
    except OSError:
        return {}


_CONCEPT_LABELS = {
    language: _load_concept_labels(path)
    for language, path in _LABELS_PATHS.items()
}


class TCAVConceptScore(BaseModel):
    concept: str
    score: float


class TCAVAnalysis(BaseModel):
    concept_scores: Dict[str, float] = Field(default_factory=dict)
    ranked_concept_scores: List[TCAVConceptScore] = Field(default_factory=list)


def _normalize_language(language: Literal["de", "en"] = "de") -> Literal["de", "en"]:
    return language if language in _LABELS_PATHS else "de"


def _humanize_tcav_concept(concept: str, language: Literal["de", "en"] = "de") -> str:
    mapped = _CONCEPT_LABELS.get(_normalize_language(language), {}).get(concept)
    if mapped:
        return mapped
    fallback = concept.rsplit("/", 1)[-1].replace("_", " ").strip()
    return fallback or concept


def humanize_tcav_concept(concept: str, language: Literal["de", "en"] = "de") -> str:
    return _humanize_tcav_concept(concept, language=language)


def _describe_score_strength(score: float, language: Literal["de", "en"] = "de") -> str:
    abs_score = abs(score)
    if abs_score >= 0.25:
        return "stark" if language == "de" else "strong"
    if abs_score >= 0.15:
        return "mittel" if language == "de" else "medium"
    return "schwach" if language == "de" else "weak"


def build_tcav_explanation_sentence(analysis: TCAVAnalysis, top_k: int = 3, language: Literal["de", "en"] = "de") -> str:
    language = _normalize_language(language)
    ranked = list(analysis.ranked_concept_scores)[: max(1, top_k)]
    if not ranked:
        return "Kein Konzept erkennbar." if language == "de" else "No concept identifiable."

    supporting = [(item, _describe_score_strength(item.score, language)) for item in ranked if item.score >= 0]
    opposing = [(item, _describe_score_strength(item.score, language)) for item in ranked if item.score < 0]

    def fmt(items: list) -> str:
        return ", ".join(f"{_humanize_tcav_concept(i.concept, language=language)} ({s})" for i, s in items)

    if language == "en":
        if supporting and opposing:
            return f"For this speaks {fmt(supporting)}, against it {fmt(opposing)}."
        if supporting:
            return f"The prediction is supported by {fmt(supporting)}."
        return f"The prediction is weakened by {fmt(opposing)}."
    else:
        if supporting and opposing:
            return f"Dafür spricht {fmt(supporting)}, dagegen {fmt(opposing)}."
        if supporting:
            return f"Die Vorhersage wird gestützt durch {fmt(supporting)}."
        return f"Die Vorhersage wird geschwächt durch {fmt(opposing)}."


def build_tcav_explanation_sentences(analysis: TCAVAnalysis, top_k: int = 3) -> dict[str, str]:
    return {
        "de": build_tcav_explanation_sentence(analysis, top_k=top_k, language="de"),
        "en": build_tcav_explanation_sentence(analysis, top_k=top_k, language="en"),
    }


def compute_tcav_analysis(input_img: np.ndarray, model_: tf.keras.models.Model, **settings: object) -> TCAVAnalysis:
    defaults = {
        "explainer": {
            "cav_dir": "/inspection/explainer/explainers/tcav/cavs",
        }
    }
    merged = dict(defaults)
    # settings may contain nested dicts; merge shallowly so API-provided values override defaults
    merged.update(settings or {})
    config = TCAVConfiguration(**merged)
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
    defaults = {
        "explainer": {
            "cav_dir": "/inspection/explainer/explainers/tcav/cavs",
        }
    }
    merged = dict(defaults)
    merged.update(settings or {})
    config = TCAVConfiguration(**merged)
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
