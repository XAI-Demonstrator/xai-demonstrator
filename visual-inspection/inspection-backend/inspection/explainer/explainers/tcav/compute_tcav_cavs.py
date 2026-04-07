from inspection.model.model import get_model
from inspection.explainer.explainers.tcav.preprocess_tcav import preprocess_batch
from inspection.explainer.explainers.tcav.tcav_calculate_cavs import compute_and_store_cavs


def main() -> None:
    """Entry point to compute and persist all TCAV CAVs for the configured concepts.

    This script is intended to be run offline. It will:

    * Load the configured model ("my_model" by default).
    * Iterate over all configured concepts and random concepts.
    * Compute CAVs for the chosen bottleneck layer.
    * Store the resulting ``.npz`` files under ``cavs/``.
    """
    concepts_root = "inspection/explainer/explainers/tcav/concept_data"
    cav_output_dir = "inspection/explainer/explainers/tcav/cavs"
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

    # At least one random concept is required for TCAV; multiple can help
    random_concepts = [
        "random_concepts/random_1",
        "random_concepts/random_2",
        "random_concepts/random_3",
    ]

    # Bottleneck layer used to extract activations for CAV training.
    bottleneck_layer_name = "global_average_pooling2d_1"

    # NOTE: The model id must exist in ``inspection/model/models`` and be
    # configured as part of the backend. For the visual inspection demo the
    # default id is "my_model".
    model = get_model("my_model")

    cav_files = compute_and_store_cavs(
        model=model,
        bottleneck_layer_name=bottleneck_layer_name,
        concepts_root=concepts_root,
        concepts=concepts,
        random_concepts=random_concepts,
        cav_output_dir=cav_output_dir,
        preprocess_fn=preprocess_batch,
    )

    print(f"CAVs written to {cav_output_dir} ({len(cav_files)} files).")


if __name__ == "__main__":
    main()