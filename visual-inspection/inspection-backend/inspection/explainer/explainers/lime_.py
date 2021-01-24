import numpy as np
import tensorflow as tf
from lime import lime_image
from opentelemetry import trace
from skimage.segmentation import mark_boundaries

_lime = lime_image.LimeImageExplainer()


def lime_explanation(input_img: np.ndarray,
                     model_: tf.keras.models.Model,
                     top_labels=5, hide_color=None, num_samples=100) -> np.ndarray:
    explanation = _lime.explain_instance(input_img.astype('double'), model_.predict,
                                         top_labels=top_labels,
                                         hide_color=hide_color,
                                         num_samples=num_samples)

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("render-explanation"):
        temp, mask = explanation.get_image_and_mask(
            explanation.top_labels[0],
            positive_only=False,
            num_features=10,
            hide_rest=False
        )
        return mark_boundaries(temp / 2 + 0.5, mask)
