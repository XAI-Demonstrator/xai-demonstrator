from typing import List, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def deprocess_mobilenet_v2_image(input_img: np.ndarray) -> np.ndarray:
    """Convert MobileNetV2 preprocessed image data back to [0, 1] RGB."""
    restored = (input_img + 1.0) / 2.0
    return np.clip(restored, 0.0, 1.0).astype(np.float32)


def _short_concept_name(concept: str) -> str:
    """Use the leaf concept name to keep overlay labels compact."""
    return concept.split("/")[-1]


def render_tcav_overlay(
    input_img: np.ndarray,
    ranked_scores: List[Tuple[str, float]],
    *,
    top_k: int,
) -> np.ndarray:
    """Render a non-spatial TCAV score panel on top of the image."""
    base_img = (deprocess_mobilenet_v2_image(input_img) * 255).astype(np.uint8)
    img = Image.fromarray(base_img)

    width, height = img.size
    shown = ranked_scores[: max(1, top_k)]

    panel_height = max(86, min(150, height // 2))
    panel_top = max(0, height - panel_height)

    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle((0, panel_top, width, height), fill=(0, 0, 0, 165))

    font = ImageFont.load_default()
    draw.text((8, panel_top + 6), "TCAV Score Visualization", fill=(255, 255, 255, 255), font=font)

    if not shown:
        draw.text((8, panel_top + 26), "No TCAV concepts available", fill=(255, 255, 255, 255), font=font)
        return np.asarray(img).astype(np.float32) / 255.0

    label_x = 8
    bar_left = max(130, width // 3)
    bar_right = width - 10
    center_x = bar_left + (bar_right - bar_left) // 2
    max_abs = max(abs(score) for _, score in shown) or 1.0

    row_start = panel_top + 26
    row_height = max(16, (panel_height - 30) // max(1, len(shown)))

    for index, (concept, score) in enumerate(shown):
        y = row_start + index * row_height
        label = _short_concept_name(concept)
        draw.text((label_x, y), label, fill=(255, 255, 255, 255), font=font)

        draw.line((bar_left, y + 8, bar_right, y + 8), fill=(255, 255, 255, 90), width=1)
        draw.line((center_x, y + 2, center_x, y + 14), fill=(255, 255, 255, 170), width=1)

        strength = int(((abs(score) / max_abs) * (bar_right - bar_left) / 2))
        if score >= 0:
            draw.rectangle((center_x, y + 4, center_x + strength, y + 12), fill=(62, 180, 137, 220))
        else:
            draw.rectangle((center_x - strength, y + 4, center_x, y + 12), fill=(220, 88, 88, 220))

        score_text = f"{score:+.3f}"
        draw.text((bar_right - 58, y), score_text, fill=(255, 255, 255, 255), font=font)

    return np.asarray(img).astype(np.float32) / 255.0


def render_tcav_score_panel(
    ranked_scores: List[Tuple[str, float]],
    *,
    top_k: int | None = None,
    width: int = 900,
) -> np.ndarray:
    """Render a standalone TCAV score visualization without overlaying the input image."""
    shown = ranked_scores if top_k is None else ranked_scores[: max(1, top_k)]
    panel_height = max(120, 54 + (len(shown) * 28))
    img = Image.new("RGBA", (width, panel_height), (18, 18, 18, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    font = ImageFont.load_default()

    draw.text((12, 8), "TCAV Concept Score Visualization", fill=(255, 255, 255, 255), font=font)

    if not shown:
        draw.text((12, 30), "No TCAV concepts available", fill=(255, 255, 255, 255), font=font)
        return np.asarray(img).astype(np.float32) / 255.0

    label_x = 12
    bar_left = max(220, width // 3)
    bar_right = width - 16
    center_x = bar_left + (bar_right - bar_left) // 2
    max_abs = max(abs(score) for _, score in shown) or 1.0

    row_start = 32
    row_height = 26

    for index, (concept, score) in enumerate(shown):
        y = row_start + index * row_height
        label = _short_concept_name(concept)
        draw.text((label_x, y), label, fill=(255, 255, 255, 255), font=font)

        draw.line((bar_left, y + 8, bar_right, y + 8), fill=(255, 255, 255, 90), width=1)
        draw.line((center_x, y + 2, center_x, y + 14), fill=(255, 255, 255, 170), width=1)

        strength = int(((abs(score) / max_abs) * (bar_right - bar_left) / 2))
        if score >= 0:
            draw.rectangle((center_x, y + 4, center_x + strength, y + 12), fill=(62, 180, 137, 220))
        else:
            draw.rectangle((center_x - strength, y + 4, center_x, y + 12), fill=(220, 88, 88, 220))

        draw.text((bar_right - 66, y), f"{score:+.3f}", fill=(255, 255, 255, 255), font=font)

    return np.asarray(img).astype(np.float32) / 255.0


