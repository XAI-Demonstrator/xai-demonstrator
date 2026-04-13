import importlib
import sys
from pathlib import Path

import numpy as np

BACKEND_ROOT = Path(__file__).resolve().parents[3]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

tcav_render = importlib.import_module("inspection.explainer.explainers.tcav.tcav_render")
deprocess_mobilenet_v2_image = tcav_render.deprocess_mobilenet_v2_image
render_tcav_overlay = tcav_render.render_tcav_overlay
render_tcav_score_panel = tcav_render.render_tcav_score_panel


def test_deprocess_mobilenet_v2_image_clips_into_unit_interval():
    raw = np.array([[[-2.0, -1.0, 0.0], [1.0, 2.0, 3.0]]], dtype=np.float32)

    out = deprocess_mobilenet_v2_image(raw)

    assert out.dtype == np.float32
    assert float(out.min()) >= 0.0
    assert float(out.max()) <= 1.0


def test_render_tcav_overlay_returns_rgb_float_image():
    input_img = np.zeros((224, 224, 3), dtype=np.float32)
    ranked_scores = [("object_concepts/camera", 0.4), ("form_concepts/round", -0.2)]

    rendered = render_tcav_overlay(input_img, ranked_scores, top_k=2)

    assert rendered.shape == input_img.shape
    assert rendered.dtype == np.float32
    assert float(rendered.min()) >= 0.0
    assert float(rendered.max()) <= 1.0
    assert not np.array_equal(rendered, deprocess_mobilenet_v2_image(input_img))


def test_render_tcav_score_panel_returns_rgb_float_image():
    ranked_scores = [("object_concepts/camera", 0.4), ("form_concepts/round", -0.2)]

    rendered = render_tcav_score_panel(ranked_scores, top_k=None)

    assert rendered.ndim == 3
    assert rendered.shape[2] == 4 or rendered.shape[2] == 3
    assert rendered.dtype == np.float32
    assert float(rendered.min()) >= 0.0
    assert float(rendered.max()) <= 1.0


