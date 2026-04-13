import numpy as np

from inspection.explainer.explainers.tcav.tcav_render import deprocess_mobilenet_v2_image, render_tcav_overlay


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

