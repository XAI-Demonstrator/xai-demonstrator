from lime import lime_image
from lime.wrappers.scikit_image import SegmentationAlgorithm
from skimage.segmentation import mark_boundaries
import base64
import cv2 
import numpy as np

def convert_explanation(explanation):
    image = (explanation*255).astype(np.uint8)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(image_rgb,(448, 448), interpolation=cv2.INTER_CUBIC)
    retval, buffer = cv2.imencode('.png', img_resized)
    encoded_image_string = base64.b64encode(buffer)
    return encoded_image_string

def explain_cnn(img, model):
    explainer = lime_image.LimeImageExplainer()
    #explanation = explainer.explain_instance(img[0].astype('double'), model.predict,  segmentation_fn =  SegmentationAlgorithm('slic', kernel_size=4, max_dist=100, ratio=0.4), top_labels=2, hide_color=False, num_samples=1000)
    explanation = explainer.explain_instance(img[0].astype('double'), model.predict,  top_labels=4, hide_color=False, num_features= 10000, num_samples=10)
    temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=False, negative_only=False,   num_features=5,  min_weight=0.0, hide_rest=False)
    return (mark_boundaries(temp , mask))
