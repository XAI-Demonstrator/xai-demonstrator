from pydantic import BaseModel
import numpy as np
import tensorflow as tf
from xaidemo.tracing import add_span_attributes, traced
from visualime.explain import explain_classification, render_explanation
from visualime.visualize import mark_boundaries


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


class VisuaLIMEConfiguration(BaseModel):
    explainer: ExplainerConfiguration = ExplainerConfiguration()
    renderer: RendererConfiguration = RendererConfiguration()

    class Config:
        extra = 'forbid'


@traced(label="compute_explanation", attributes={"explanation.method": "visualime"})
def visualime_explanation(input_img: np.ndarray,
                          model_: tf.keras.models.Model,
                          **settings) -> np.ndarray:
    config = VisuaLIMEConfiguration(**settings)

    # Convert the image from the range [-1, 1] to [0, 255]
    input_img = (input_img / 2 + 0.5) * 255
    input_img = input_img.astype(np.uint8)

    segment_mask, segment_weights = explain_classification(image=input_img, predict_fn=model_,
                                                           segmentation_method=config.explainer.segmentation_method,
                                                           num_of_samples=config.explainer.num_samples, )

    img_pil = render_explanation(image=input_img, segment_mask=segment_mask, segment_weights=segment_weights,
                                 positive=(0, 255, 0), negative=(255, 0, 0))
    # Mark the boundaries of the segments and convert the image from RGBA to RGB
    img_np = mark_boundaries(np.array(img_pil)[:, :, :3], segment_mask)
    return img_np
