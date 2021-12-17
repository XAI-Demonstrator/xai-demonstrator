# new explainer
import numpy as np
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from skimage.filters import sobel
from skimage.color import rgb2gray


# method to create segments out of a loaded picture using different methods and settings
def create_segments(img: np.ndarray, seg_method: str, settings: list) -> np.ndarray:
    # currently, using fixed settings
    if seg_method == "felzenszwalb":
        return felzenszwalb(image=img, scale=250, sigma=0.6, min_size=45)

    if seg_method == "slic":
        return slic(image=img, n_segments=250, compactness=2, convert2lab=True, sigma=1, start_label=1)

    if seg_method == "quickshift":
        return quickshift(img, kernel_size=5, max_dist=6, ratio=0.7)  # mb sigma = 6

    if seg_method == "watershed":
        gradient = sobel(rgb2gray(img))
        return watershed(gradient, markers=250, compactness=0.001)

    else:
        raise ValueError("{} is not a valid segmentation method".format(seg_method))
