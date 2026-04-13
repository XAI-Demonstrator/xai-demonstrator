import importlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
from PIL import Image

TESTS_ROOT = Path(__file__).resolve().parent
BACKEND_ROOT = TESTS_ROOT.parent / "inspection-backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

settings = importlib.import_module("inspection.config").settings
model_module = importlib.import_module("inspection.model.model")
predict_module = importlib.import_module("inspection.model.predict")
tcav_module = importlib.import_module("inspection.explainer.explainers.tcav_")
tcav_render_module = importlib.import_module("inspection.explainer.explainers.tcav.tcav_render")


def _tcav_settings(cav_dir: Path) -> Dict[str, Any]:
    return {
        "explainer": {
            "bottleneck_layer": "global_average_pooling2d_1",
            "cav_dir": str(cav_dir),
            "cav_manifest_filename": "cav_manifest.json",
        },
        "renderer": {
            "top_k_concepts": 3,
            "return_heatmap": True,
        },
    }


def _iter_asset_images(assets_dir: Path) -> List[Path]:
    allowed = {".png", ".jpg", ".jpeg"}
    return sorted(
        p
        for p in assets_dir.iterdir()
        if p.is_file() and p.suffix.lower() in allowed and not p.stem.endswith("_tcav")
    )


def _result_dir_name(image_path: Path) -> str:
    return f"{image_path.stem}_{image_path.suffix.lower().lstrip('.')}"


def _save_png(image_array: np.ndarray, output_path: Path) -> None:
    png_image = Image.fromarray((np.clip(image_array, 0.0, 1.0) * 255).astype(np.uint8))
    png_image.save(output_path)


def run_tcav_on_image(
    image_path: Path,
    cav_dir: Path,
    results_root: Path,
    model,
    preprocess_fn,
) -> bool:
    image_result_dir = results_root / _result_dir_name(image_path)
    image_result_dir.mkdir(parents=True, exist_ok=True)

    copied_input = image_result_dir / f"input{image_path.suffix.lower()}"
    shutil.copy2(image_path, copied_input)

    tcav_settings = _tcav_settings(cav_dir)
    try:
        with Image.open(image_path) as input_image:
            explainer_input = preprocess_fn(input_image)[0]
            analysis = tcav_module.compute_tcav_analysis(explainer_input, model, **tcav_settings)

            top_k = max(1, tcav_settings["renderer"]["top_k_concepts"])
            top_scores = [(score.concept, score.score) for score in analysis.ranked_concept_scores[:top_k]]
            if tcav_settings["renderer"]["return_heatmap"]:
                output_image_array = tcav_render_module.render_tcav_overlay(
                    explainer_input,
                    top_scores,
                    top_k=top_k,
                )
            else:
                output_image_array = tcav_render_module.deprocess_mobilenet_v2_image(explainer_input)

            output_image = image_result_dir / "tcav_output.png"
            _save_png(output_image_array, output_image)

            result = {
                "schema_version": 1,
                "image_name": image_path.name,
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "concept_scores": analysis.concept_scores,
                "ranked_concept_scores": [score.model_dump() for score in analysis.ranked_concept_scores],
            }

        result_json = image_result_dir / "result.json"
        with result_json.open("w", encoding="utf-8") as file_obj:
            json.dump(result, file_obj, indent=2, ensure_ascii=True)
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"[TCAV] ERROR for {image_path.name}: {exc}")
        return False


def run_tcav_on_assets() -> None:
    assets_dir = TESTS_ROOT / "assets"
    results_root = TESTS_ROOT / "test_results"
    cav_dir = BACKEND_ROOT / "inspection" / "explainer" / "explainers" / "tcav" / "cavs"

    if not assets_dir.exists():
        raise FileNotFoundError(f"Assets directory not found: {assets_dir}")
    if not cav_dir.exists():
        raise FileNotFoundError(f"CAV directory not found: {cav_dir}")

    results_root.mkdir(parents=True, exist_ok=True)
    images = _iter_asset_images(assets_dir)
    if not images:
        raise FileNotFoundError(f"No supported images found in: {assets_dir}")

    model = model_module.get_model(settings.default_model)
    preprocess_fn = predict_module.preprocess

    print(f"[TCAV] Processing {len(images)} images from: {assets_dir}")
    successful = 0

    for image_path in images:
        print(f"[TCAV] Running explanation for: {image_path.name}")
        if run_tcav_on_image(image_path, cav_dir, results_root, model, preprocess_fn):
            successful += 1

    print(f"[TCAV] Completed: {successful}/{len(images)} successful.")

if __name__ == "__main__":
    run_tcav_on_assets()
