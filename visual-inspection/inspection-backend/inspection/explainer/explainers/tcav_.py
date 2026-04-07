import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import tensorflow as tf
from pydantic import BaseModel
from xaidemo.tracing import traced

EPSILON = 1e-8


class TCAVExplainerConfiguration(BaseModel):
    concepts: Optional[List[str]] = None
    random_concepts: Optional[List[str]] = None
    bottleneck_layer: str = "global_average_pooling2d_1"
    num_random_experiments: int = 10
    cav_dir: str
    concepts_root: str

    class Config:
        extra = "forbid"


class TCAVRendererConfiguration(BaseModel):
    return_heatmap: bool = True
    top_k_concepts: int = 3

    class Config:
        extra = "forbid"


class TCAVConfiguration(BaseModel):
    explainer: TCAVExplainerConfiguration
    renderer: TCAVRendererConfiguration = TCAVRendererConfiguration()

    class Config:
        extra = "forbid"


def _safe_name(name: str) -> str:
    return name.replace("/", "_").replace("\\", "_")


def _discover_concepts_from_root(concepts_root: str) -> Tuple[List[str], List[str]]:
    concepts: List[str] = []
    randoms: List[str] = []

    if not os.path.isdir(concepts_root):
        return concepts, randoms

    random_root = os.path.join(concepts_root, "random_concepts")
    if os.path.isdir(random_root):
        for child in sorted(os.listdir(random_root)):
            p = os.path.join(random_root, child)
            if os.path.isdir(p):
                randoms.append(f"random_concepts/{child}")

    for group in sorted(os.listdir(concepts_root)):
        if group == "random_concepts":
            continue
        group_path = os.path.join(concepts_root, group)
        if not os.path.isdir(group_path):
            continue
        for child in sorted(os.listdir(group_path)):
            p = os.path.join(group_path, child)
            if os.path.isdir(p):
                concepts.append(f"{group}/{child}")

    return sorted(concepts), sorted(randoms)


def _resolve_explainer_config(config: TCAVExplainerConfiguration) -> TCAVExplainerConfiguration:
    concepts = config.concepts
    randoms = config.random_concepts

    if concepts is None or randoms is None:
        discovered_concepts, discovered_randoms = _discover_concepts_from_root(config.concepts_root)
        if concepts is None:
            concepts = discovered_concepts
        if randoms is None:
            randoms = discovered_randoms

    if not concepts:
        raise ValueError(
            "No concepts configured or discovered. Provide explainer.concepts or a valid concepts_root.",
        )
    if not randoms:
        raise ValueError(
            "No random concepts configured or discovered. Provide explainer.random_concepts or random_concepts/*.",
        )

    update_data = {"concepts": concepts, "random_concepts": randoms}
    if hasattr(config, "model_copy"):
        return config.model_copy(update=update_data)
    return config.copy(update=update_data)


def load_cavs_for_config(config: TCAVExplainerConfiguration) -> Dict[str, np.ndarray]:
    """Load precomputed CAV vectors for all configured concept/random pairs."""
    concepts = config.concepts or []
    randoms = config.random_concepts or []
    cavs: Dict[str, np.ndarray] = {}
    missing_pairs = 0

    for concept in concepts:
        for rnd in randoms:
            filename = f"{_safe_name(concept)}__vs__{_safe_name(rnd)}__{config.bottleneck_layer}.npz"
            path = os.path.join(config.cav_dir, filename)
            if not os.path.exists(path):
                missing_pairs += 1
                continue
            with np.load(path) as data:
                cavs[f"{concept}__vs__{rnd}"] = data["cav"]

    if not cavs:
        raise FileNotFoundError(f"No CAVs found in '{config.cav_dir}' for bottleneck '{config.bottleneck_layer}'.")
    if missing_pairs:
        print(f"[TCAV] Missing {missing_pairs} concept/random CAV files; continuing with available files.")
    return cavs


def _compute_concept_scores(
        acts_flat: np.ndarray,
        cavs: Dict[str, np.ndarray],
) -> Dict[str, float]:
    """Compute one score per concept (max over random counterparts)."""
    concept_scores: Dict[str, float] = {}
    acts_norm = float(np.linalg.norm(acts_flat))

    for key, cav in cavs.items():
        concept_name = key.split("__vs__", maxsplit=1)[0]
        cav_flat = cav.reshape(-1)
        cav_norm = float(np.linalg.norm(cav_flat))
        denom = acts_norm * cav_norm + EPSILON
        score = float(np.dot(acts_flat, cav_flat)) / denom

        prev = concept_scores.get(concept_name)
        concept_scores[concept_name] = score if prev is None else max(prev, score)

    return concept_scores


@traced(label="compute_explanation", attributes={"explanation.method": "tcav"})
def tcav_explanation(
        input_img: np.ndarray,
        model_: tf.keras.models.Model,
        **settings: Dict[str, object],
) -> np.ndarray:
    """Compute TCAV concept scores for a single input."""
    config = TCAVConfiguration(**settings)
    explainer_config = _resolve_explainer_config(config.explainer)
    cavs = load_cavs_for_config(explainer_config)

    # 1) Build bottleneck model
    bottleneck_layer = explainer_config.bottleneck_layer
    bottleneck_output = model_.get_layer(bottleneck_layer).output
    bottleneck_model = tf.keras.Model(inputs=model_.inputs, outputs=bottleneck_output)

    # 2) Compute bottleneck activations for this input (add batch dimension)
    acts = bottleneck_model.predict(input_img[np.newaxis, ...], verbose=0)
    acts_flat = acts.reshape(-1)

    # 3) Compute one score per concept (max over concept-vs-random pairs)
    concept_scores = _compute_concept_scores(acts_flat, cavs)

    if not concept_scores:
        print("[TCAV] WARING - No Concept scores computed")
        return input_img

    # 4) Build a full ranking and pick top-k concepts by absolute score
    ranked_all = sorted(concept_scores.items(), key=lambda kv: abs(kv[1]), reverse=True)
    k = max(1, config.renderer.top_k_concepts)
    top = ranked_all[:k]

    # Debug: log top-k and full ranking for inspection.
    print("[TCAV] Concept scores (top-k):", top)
    print("[TCAV] Concept scores (all):", ranked_all)

    return input_img
