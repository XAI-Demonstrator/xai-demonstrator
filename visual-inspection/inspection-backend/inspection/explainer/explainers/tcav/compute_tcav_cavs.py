from inspection.model.model import get_model
from inspection.explainer.explainers.tcav.preprocess_tcav import preprocess_batch
from inspection.explainer.explainers.tcav.tcav_calculate_cavs import compute_and_store_cavs

def main():
    concepts_root = "inspection/explainer/explainers/tcav/concept_data"
    cav_output_dir = r".\cavs"

    concepts = [
        "form_concepts/round",
        "form_concepts/rectangular",
        "object_concepts/phone",
        "object_concepts/keyboard",
        "object_concepts/camera",
        "object_concepts/cup",
        "object_concepts/glasses",
        "object_concepts/keys",
        "object_concepts/mouse",
        "object_concepts/notebook",
        "visual_concepts/screen_surface",
        "visual_concepts/metal",
        "visual_concepts/paper",
        "visual_concepts/white",
        "visual_concepts/glass",
    ]

    random_concepts = [
        "random_concepts/random_1",
        "random_concepts/random_2",
        "random_concepts/random_3",
    ]     # NOTE: mind. one random-concept is required for TCAV, but can be more (e.g. random_2, random_3, ...)

    bottleneck_layer_name = "global_average_pooling2d_1"

    model = get_model("my_model")  # todo: check and may load from settings

    cav_files = compute_and_store_cavs(
        model=model,
        bottleneck_layer_name=bottleneck_layer_name,
        concepts_root=concepts_root,
        concepts=concepts,
        random_concepts=random_concepts,
        cav_output_dir=cav_output_dir,
        preprocess_fn=preprocess_batch,
    )

    print("CAVs written to {}".format(cav_output_dir))

if __name__ == "__main__":
    main()