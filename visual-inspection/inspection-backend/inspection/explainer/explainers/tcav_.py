import os
from typing import List, Dict

import numpy as np
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
    cavs = {}
    for concept in config.concepts:
        for rnd in config.random_concepts:
            filename = f"{concept}__vs__{rnd}__{config.bottleneck_layer}.npz"
            path = os.path.join(config.cav_dir, filename)
            data = np.load(path)
            cavs[f"{concept}__vs__{rnd}"] = data["cav"]
    return cavs

@traced(label="compute_explanation", attributes={"explanation.method": "tcav"})
def tcav_explanation(input_img: np.ndarray,
                     model_: tf.keras.models.Model,
                     **settings) -> np.ndarray:
    config = TCAVConfiguration(**settings)
    cavs = load_cavs_for_config(config.explainer)
    # TODO: TCAV-Score + Heatmap mit Hilfe von `model_` und `cavs` berechnen
    return input_img
