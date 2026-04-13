import base64
from pathlib import Path

from inspection.config import settings
from inspection.explainer import explain


def run_tcav_on_example(image_path: Path) -> None:
    repo_root = Path(__file__).resolve().parent.parent
    backend_root = repo_root / "inspection-backend"
    cav_dir = backend_root / "inspection" / "explainer" / "explainers" / "tcav" / "cavs"

    print(f"[TCAV] Loading example image from: {image_path}")
    with image_path.open("rb") as f:
        explanation = explain.explain(
            f,
            model_id=settings.default_model,
            method="tcav",
            settings={
                "explainer": {
                    "bottleneck_layer": "global_average_pooling2d_1",
                    "cav_dir": str(cav_dir),
                    "cav_manifest_filename": "cav_manifest.json",
                },
                "renderer": {
                    "top_k_concepts": 3,
                    "return_heatmap": True,
                },
            },
        )

    data_url = explanation.image
    prefix = b"data:image/png;base64,"
    if not data_url.startswith(prefix):
        raise ValueError("Unexpected image format returned from explain().")

    print("[TCAV] Decoding PNG data URL ...")
    png_bytes = base64.b64decode(data_url[len(prefix):])

    output_path = image_path.with_name(image_path.stem + "_tcav.png")
    with output_path.open("wb") as out_f:
        out_f.write(png_bytes)

    print(f"[TCAV] TCAV explanation image written to: {output_path}")



if __name__ == "__main__":
    # Resolve example image relative to this script directory.
    example_image = Path(__file__).resolve().parent / "images" / "example_coffe-cup.png"
    if not example_image.exists():
        raise FileNotFoundError(f"Example image not found: {example_image}")
    run_tcav_on_example(example_image)
