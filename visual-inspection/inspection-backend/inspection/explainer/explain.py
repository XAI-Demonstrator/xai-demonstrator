from typing import IO, Tuple

import numpy as np
from PIL import Image
from lime import lime_image
from skimage.segmentation import mark_boundaries

from ..model.model import model
from ..model.predict import preprocess

explainer = lime_image.LimeImageExplainer()


def generate_output_image(raw_image: np.ndarray, size: Tuple[int, int]) -> Image:
    exp_image = Image.fromarray((255 * raw_image).astype(np.uint8))
    return exp_image.resize(size, Image.BICUBIC)


def explain(image_file: IO[bytes]) -> Image:
    input_image = Image.open(image_file)

    explainer_input = preprocess(input_image)[0]

    explanation = explainer.explain_instance(explainer_input.astype('double'),
                                             model.predict,
                                             top_labels=5,
                                             hide_color=None,
                                             num_samples=100)

    temp, mask = explanation.get_image_and_mask(
        explanation.top_labels[0],
        positive_only=False,
        num_features=10,
        hide_rest=False
    )
    raw_image = mark_boundaries(temp / 2 + 0.5, mask)

    return generate_output_image(raw_image, input_image.size)
