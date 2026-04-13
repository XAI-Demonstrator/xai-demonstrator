from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TCAVExplainerConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    concepts: Optional[List[str]] = None
    random_concepts: Optional[List[str]] = None
    bottleneck_layer: str = "global_average_pooling2d_1"
    num_random_experiments: int = Field(default=10, ge=1)
    cav_dir: str
    concepts_root: Optional[str] = None
    cav_manifest_filename: str = "cav_manifest.json"


class TCAVRendererConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    return_heatmap: bool = True
    top_k_concepts: int = Field(default=3, ge=1)


class TCAVConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    explainer: TCAVExplainerConfiguration
    renderer: TCAVRendererConfiguration = Field(default_factory=TCAVRendererConfiguration)


class CAVLoadEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    concept: str
    random_concept: str
    bottleneck_layer: str
    filename: str
    file_path: str

