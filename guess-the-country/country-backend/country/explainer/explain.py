from lime import lime_image
from lime.wrappers.scikit_image import SegmentationAlgorithm
from skimage.segmentation import mark_boundaries


def explain_cnn(img, model):
    explainer = lime_image.LimeImageExplainer()
    explanation = explainer.explain_instance(img[0].astype('double'), model.predict,
                                             segmentation_fn=SegmentationAlgorithm('slic', kernel_size=4, max_dist=100,
                                                                                   ratio=0.4), top_labels=2,
                                             hide_color=False, num_samples=1000)
    temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=False, negative_only=False,
                                                num_features=5, hide_rest=False)
    print(mark_boundaries(temp, mask))
    return (mark_boundaries(temp, mask))
