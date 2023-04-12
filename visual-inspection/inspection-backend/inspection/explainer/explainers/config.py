from pydantic import BaseModel


class ExplainerConfiguration(BaseModel):
    top_labels: int = 5
    num_samples: int = 100
    num_features: int = 10000
    segmentation_method: str = 'felzenszwalb'

    class Config:
        extra = 'forbid'


class RendererConfiguration(BaseModel):
    num_features: int = 5
    min_weight: float = 0.0
    positive_only: bool = False

    class Config:
        extra = 'forbid'


class LIMEConfiguration(BaseModel):
    explainer: ExplainerConfiguration = ExplainerConfiguration()
    renderer: RendererConfiguration = RendererConfiguration()

    class Config:
        extra = 'forbid'