import os
from typing import List, Dict

import numpy as np
import tensorflow as tf
from pydantic import BaseModel
from xaidemo.tracing import traced


class TCAVExplainerConfiguration(BaseModel):
    concepts: List[str]
    random_concepts: List[str]
    bottleneck_layer: str
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


def load_cavs_for_config(config: TCAVExplainerConfiguration) -> Dict[str, np.ndarray]:
    cavs: Dict[str, np.ndarray] = {}
    for concept in config.concepts:
        for rnd in config.random_concepts:
            # CAV filenames are stored with sanitized names ("/" and "\\" replaced by "_")
            safe_concept = concept.replace("/", "_").replace("\\", "_")
            safe_rnd = rnd.replace("/", "_").replace("\\", "_")
            filename = f"{safe_concept}__vs__{safe_rnd}__{config.bottleneck_layer}.npz"
            path = os.path.join(config.cav_dir, filename)
            if not os.path.exists(path):
                raise FileNotFoundError(f"CAV file not found for concept pair '{concept}' vs '{rnd}': {path}")
            data = np.load(path)
            cavs[f"{concept}__vs__{rnd}"] = data["cav"]
    return cavs


@traced(label="compute_explanation", attributes={"explanation.method": "tcav"})
def tcav_explanation(input_img: np.ndarray,
                     model_: tf.keras.models.Model,
                     **settings) -> np.ndarray:
    """Minimal TCAV explainer stub.

    This currently only loads the configured CAVs to validate the configuration
    and CAV storage. It returns the original input image unchanged so that the
    end-to-end API and tests continue to work while the full TCAV scoring and
    rendering logic is being implemented.
    """
    config = TCAVConfiguration(**settings)
    # Load CAVs to ensure configuration and file paths are valid; will raise
    # early if anything is misconfigured.
    _ = load_cavs_for_config(config.explainer)

    # TODO: Use `model_` and the loaded CAVs to compute TCAV scores and render
    # a heatmap-like explanation image instead of returning the input.
    return input_img
