"""XAI Demonstrator LIME explainer"""
from typing import Dict

import numpy as np
import tensorflow as tf
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed


def create_segments(img: np.ndarray, seg_method: str, settings: Dict) -> np.ndarray:
    """
    create segments out of a loaded picture using different methods and settings

    Parameters
    ----------
    img
    seg_method
    settings

    Returns
    -------

    """
    # currently, using fixed settings
    if seg_method == "felzenszwalb":
        return felzenszwalb(image=img, scale=250, sigma=0.6, min_size=45)

    if seg_method == "slic":
        return slic(image=img, n_segments=250, compactness=2, convert2lab=True, sigma=1, start_label=1)

    if seg_method == "quickshift":
        return quickshift(image=img, kernel_size=5, max_dist=6, ratio=0.7)  # mb sigma = 6

    if seg_method == "watershed":
        gradient = sobel(rgb2gray(img))
        return watershed(image=gradient, markers=250, compactness=0.001)

    else:
        raise ValueError("{} is not a valid segmentation method".format(seg_method))


def generate_samples(segment_mask: np.ndarray, num_of_samples: int, p: float) -> np.ndarray:
    """
    determine which segments are displayed for each sample

    Parameters
    ----------
    segment_mask : np.ndarray
        The mask generated by `create_segments()`: An array of the same dimension as the image
    num_of_samples : int
        The number of samples to generate
    p : float
        The probability for each segment to be replaced
    Returns
    -------
    samples : np.ndarray
        A two-dimensional array of dimension (num_of_samples, number_of_segments)
    """
    num_of_segments = np.max(segment_mask) + 1
    return np.array([np.random.binomial(n=1, p=p, size=num_of_segments) for i in range(num_of_samples)])


def generate_images(image: np.ndarray, segment_mask: np.ndarray, samples: np.ndarray) -> np.ndarray:
    """Generating example images with each excluded segments in black


    Parameters
    ----------
    image
    segment_mask
    samples

    Returns
    -------

    """
    images = np.zeros((samples.shape[0],) + image.shape)
    segment_mask = segment_mask.reshape(image.shape[:2] + (1,))
    segment_ids = np.unique(segment_mask)
    samples_enu = enumerate(samples)
    for i, sample in samples_enu:
        mask = np.zeros(image.shape)
        for s_id in segment_ids:
            if sample[s_id]:
                mask += segment_mask == s_id
        images[i] = mask * image
    return images


def predict_images(images: np.ndarray, model_: tf.keras.models.Model) -> np.ndarray:
    """

    Parameters
    ----------
    images
    model_

    Returns
    -------

    """
    predictions = []
    for i in images:
        tst_pic = np.expand_dims(i, axis=0)
        tst_pic = tst_pic[:, :, :, :3]
        tst_pic = tf.keras.applications.mobilenet_v2.preprocess_input(tst_pic)
        prediction = predict_class(tst_pic, model_=model_)
        predictions.append(prediction)
    print(predictions)
    return np.array([])
