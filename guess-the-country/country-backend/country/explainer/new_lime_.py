"""XAI Demonstrator LIME explainer"""
from typing import Dict
import numpy as np
import tensorflow as tf
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
from sklearn.linear_model import Lasso, BayesianRidge, LinearRegression
from ..config import settings


def explain_image(img: np.ndarray, seg_method: str, seg_settings: Dict, num_of_samples: int, samples_p: float,
                  model_: tf.keras.models.Model, threshold: float, volume: int, colour: str,
                  transparency: float) -> np.ndarray:
    segment_mask = create_segments(img=img, seg_method=seg_method, settings=seg_settings)
    samples_theo = generate_samples(segment_mask=segment_mask, num_of_samples=num_of_samples, p=samples_p)
    samples_imgs = generate_images(image=img, segment_mask=segment_mask, samples=samples_theo)
    samples_imgs_predictions = predict_images(images=samples_imgs, model_=model_)
    weighted_segments = weigh_segments(samples=samples_theo, predictions=samples_imgs_predictions)
    visual_explanation = generate_visual_explanation(weighted_segments=weighted_segments, segment_mask=segment_mask,
                                                     image=img, threshold=threshold, volume=volume, colour=colour,
                                                     transparency=transparency)

    return visual_explanation


#returns indices of segments to be shown in explanation
def explain_image_for_seg_occ_test(img: np.ndarray, seg_method: str, seg_settings: Dict, num_of_samples: int, samples_p: float,
                  model_: tf.keras.models.Model, threshold: float, volume: int, colour: str,
                  transparency: float, segment_mask: np.ndarray) -> np.ndarray:
    #segment_mask = create_segments(img=img, seg_method=seg_method, settings=seg_settings)
    samples_theo = generate_samples(segment_mask=segment_mask, num_of_samples=num_of_samples, p=samples_p)
    samples_imgs = generate_images(image=img, segment_mask=segment_mask, samples=samples_theo)
    samples_imgs_predictions = predict_images(images=samples_imgs, model_=model_)
    weighted_segments = weigh_segments(samples=samples_theo, predictions=samples_imgs_predictions)
    indices = generate_visual_explanation_for_seg_occ_test(weighted_segments=weighted_segments, segment_mask=segment_mask,
                                                     image=img, threshold=threshold, volume=volume, colour=colour,
                                                     transparency=transparency)

    return indices


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
    # TODO: Allow for changes in settings
    # TODO: Reduce to practically useful segmentation variants
    if seg_method == "felzenszwalb":
        return felzenszwalb(image=img, scale=250, sigma=0.6, min_size=45)

    if seg_method == "slic":
        # start_label = 0 vs start_label = 1
        return slic(image=img, n_segments=250, compactness=2, convert2lab=True, sigma=1, start_label=0)

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
    org_img_sample = np.ones((1, np.unique(segment_mask).size + 1))
    # append a full 1's sample to generate and predict the original image later on to avoid variance
    return np.append(np.random.binomial(n=1, p=p, size=(num_of_samples, np.unique(segment_mask).size + 1)),
                     org_img_sample, axis=0)


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

    res = np.ones(shape=(samples.shape[0], segment_mask.shape[0], segment_mask.shape[0]))
    for k in range(segment_mask.shape[0]):
        res[:, :, k] = samples[:, segment_mask[:, k][:]]
    return res.reshape((samples.shape[0], segment_mask.shape[0], segment_mask.shape[0], 1)) * image


def predict_images(images: np.ndarray, model_: tf.keras.models.Model) -> np.ndarray:
    """
    Parameters
    ----------
    images : np.ndarray
        Images as an array of dimension (num_of_samples, IMG_SIZE, IMG_SIZE, 3)
    model_ : tf.keras.models.Model
        A tf.keras model that takes an input of size (IMG_SIZE, IMG_SIZE, 3)
    Returns
    -------
    An array of size (num_of_samples, output_dimension)
    """
    return model_.predict(images, batch_size=settings.batch_size)


def weigh_segments(samples: np.ndarray, predictions: np.ndarray) -> np.ndarray:
    """Generating list of coefficients to weigh segments
    Parameters
    ----------
    samples
    predictions
    Returns
    -------
    Array of size (num_of_segments)
    """
    # decide which linear regression model to use
    models = [BayesianRidge(), Lasso(), LinearRegression()]
    model = models[0]
    # get the  prediction-Id/column from the original image
    prev_label_id = np.bincount(np.argmax(predictions, axis=1)).argmax()

    # isolate the column from predictions
    p_column = predictions[:-1, prev_label_id]

    model.fit(samples[:-1], p_column)
    return model.coef_


def generate_visual_explanation(weighted_segments: np.ndarray, segment_mask: np.ndarray, image: np.ndarray,
                                threshold: float, volume: int, colour: str, transparency:float = 0) -> np.ndarray:
    """Generating image with visual explanation
    Parameters
    ----------
    weighted_segment
    segment_mask
    image
    threshold
    volume
    colour
    transparency
    Returns
    -------
    """
    # set explanation colour
    colours = {"green": [0,255,0], "blue": [38, 55, 173], "red": [173, 38, 38], "white": [255, 255, 255],
               "black": [0, 0, 0]}
    colour = colour.lower()
    if colour not in colours.keys():
        colour = "green"

    # handle outliers
    """
    weighted_segments = np.where(weighted_segments > 1.0, 1, weighted_segments)
    weighted_segments = np.where(weighted_segments < -1.0, -1, weighted_segments)
    # normalize coefficients: coefficient_i ∈ [0.0, 1.0]
    n_weighted_segments = (weighted_segments - weighted_segments.min()) / (
            weighted_segments.max() - weighted_segments.min())
    """
    n_weighted_segments = 1/(1+np.exp(-weighted_segments))

    # check if volume is bigger than the amount of segments
    max_volume = len(np.unique(segment_mask))
    if volume > max_volume:
        volume = max_volume

    # differentiate n_weighted_segments with respect to threshold and volume
    # values less than max(limit, threshold) are set to 0
    limit = np.sort(np.unique(n_weighted_segments))[-volume]
    n_d_weighted_segments = np.where(n_weighted_segments >= max(limit, threshold), n_weighted_segments,
                                     0)
    # manipulate the original image (quick and dirty)
    c = np.array(colours[colour])
    image_c = image.copy()
    indices = np.argwhere(n_d_weighted_segments != 0)
   
    for i, row in enumerate(segment_mask):
        for j, el in enumerate(row):
            if el in indices:
                image_c[i, j] = ((round(n_d_weighted_segments[el], 1) * c / 127.5) - 1)

    return image_c * transparency + image * (1-transparency)


def generate_visual_explanation_for_seg_occ_test(weighted_segments: np.ndarray, segment_mask: np.ndarray, image: np.ndarray,
                                threshold: float, volume: int, colour: str, transparency:float = 0) -> np.ndarray:
    """Generating image with visual explanation
    Parameters
    ----------
    weighted_segment
    segment_mask
    image
    threshold
    volume
    colour
    transparency
    Returns
    -------
    """
    # set explanation colour
    colours = {"green": [0,255,0], "blue": [38, 55, 173], "red": [173, 38, 38], "white": [255, 255, 255],
               "black": [0, 0, 0]}
    colour = colour.lower()
    if colour not in colours.keys():
        colour = "green"

    # handle outliers
    """
    weighted_segments = np.where(weighted_segments > 1.0, 1, weighted_segments)
    weighted_segments = np.where(weighted_segments < -1.0, -1, weighted_segments)
    # normalize coefficients: coefficient_i ∈ [0.0, 1.0]
    n_weighted_segments = (weighted_segments - weighted_segments.min()) / (
            weighted_segments.max() - weighted_segments.min())
    """
    n_weighted_segments = 1/(1+np.exp(-weighted_segments))

    # check if volume is bigger than the amount of segments
    max_volume = len(np.unique(segment_mask))
    if volume > max_volume:
        volume = max_volume

    # differentiate n_weighted_segments with respect to threshold and volume
    # values less than max(limit, threshold) are set to 0
    limit = np.sort(np.unique(n_weighted_segments))[-volume]
    n_d_weighted_segments = np.where(n_weighted_segments >= max(limit, threshold), n_weighted_segments,
                                     0)
    # manipulate the original image (quick and dirty)
    c = np.array(colours[colour])
    image_c = image.copy()
    indices = np.argwhere(n_d_weighted_segments != 0)
    return indices
   