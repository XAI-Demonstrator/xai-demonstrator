import numpy as np
import tensorflow as tf
from visualime.explain import explain_classification, render_explanation

from .config import LIMEConfiguration


def mark_boundaries(img: np.ndarray,
                    mask: np.ndarray,
                    color: tuple = (255, 0, 0,
                                    255)) -> np.ndarray:  # TODO mark only the boundaries adjacent to the highlighted sgements
    for i in range(1, mask.shape[0] - 1):
        for j in range(1, mask.shape[1] - 1):
            if mask[i, j] != mask[i - 1, j]:
                img[i, j] = color
            elif mask[i, j] != mask[i, j - 1]:
                img[i, j] = color
    return img


def visuallime_explanation(input_img: np.ndarray,
                           model_: tf.keras.models.Model,
                           **settings) -> np.ndarray:
    config = LIMEConfiguration(**settings)

    # Convert the image from the range [-1, 1] to [0, 255]
    input_img = (input_img / 2 + 0.5) * 255
    input_img = input_img.astype(np.uint8)

    segment_mask, segment_weights = explain_classification(image=input_img, predict_fn=model_,
                                                           segmentation_method="felzenszwalb",
                                                           num_of_samples=128)

    img_pil = render_explanation(image=input_img, segment_mask=segment_mask, segment_weights=segment_weights)
    # Mark the boundaries of the segments and convert the image from RGBA to RGB
    img_np = mark_boundaries(np.array(img_pil), segment_mask)[:, :, :3]

    return img_np