import numpy as np
import tensorflow as tf
from lime import lime_image
from skimage.segmentation import mark_boundaries
from xaidemo.tracing import traced
from .config import LIMEConfiguration, RendererConfiguration

_lime = lime_image.LimeImageExplainer()


@traced(label="compute_explanation", attributes={"explanation.method": "lime"})
def lime_explanation(input_img: np.ndarray,
                     model_: tf.keras.models.Model,
                     **settings) -> np.ndarray:
    config = LIMEConfiguration(**settings)

    explanation = _lime.explain_instance(input_img.astype("double"), model_.predict,
                                         top_labels=config.explainer.top_labels,
                                         num_features=config.explainer.num_features,
                                         num_samples=config.explainer.num_samples)

    return render_explanation(explanation, config.renderer)


@traced
def render_explanation(explanation: lime_image.ImageExplanation,
                       config: RendererConfiguration):
    image, mask = explanation.get_image_and_mask(
        explanation.top_labels[0],
        positive_only=config.positive_only,
        negative_only=False,
        num_features=config.num_features,
        min_weight=config.min_weight,
        hide_rest=False
    )

    return (mark_boundaries(image / 2 + 0.5, mask) * 255).astype("uint8")
