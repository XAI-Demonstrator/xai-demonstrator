from inspection.explainer.explainers.tcav.preprocess_tcav import preprocess_batch
from inspection.explainer.explainers.tcav.tcav_calculate_cavs import compute_and_store_cavs
from inspection.model.model import get_model


def main() -> None:
    """Compute and persist TCAV CAVs for configured concept sets."""
    concepts_root = "inspection/explainer/explainers/tcav/concept_data"
    cav_output_dir = "inspection/explainer/explainers/tcav/cavs"
    concepts = [
        # form concepts
        "form_concepts/compact_rounded",
        "form_concepts/cylindrical",
        "form_concepts/oval",
        "form_concepts/rectangular",
        "form_concepts/round",
        # Feature concepts
        "feature_concepts/circular_opening",
        "feature_concepts/has_handle",
        "feature_concepts/has_keys_buttons",
        "feature_concepts/has_lens",
        "feature_concepts/has_screen",
    ]

    # At least one random concept is required for TCAV; multiple can help
    random_concepts = [
        "random_concepts/random_1",
        "random_concepts/random_2",
        "random_concepts/random_3",
        "random_concepts/random_4",
        "random_concepts/random_5",
        "random_concepts/random_6",
        "random_concepts/random_7",
    ]

    bottleneck_layer_name = "global_average_pooling2d_1"

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
