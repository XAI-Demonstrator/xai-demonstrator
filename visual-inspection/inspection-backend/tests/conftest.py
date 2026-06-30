import io

import png
import pytest

from inspection.api import EXPLAINERS


def pytest_configure(config):
    config.addinivalue_line("markers", "lime: tests that require LIME to be active")
    config.addinivalue_line("markers", "tcav: tests that require TCAV to be active")


def pytest_collection_modifyitems(config, items):
    for item in items:
        if "lime" in item.keywords and "lime" not in EXPLAINERS:
            item.add_marker(pytest.mark.skip(reason="LIME is not an active explainer"))
        if "tcav" in item.keywords and "tcav" not in EXPLAINERS:
            item.add_marker(pytest.mark.skip(reason="TCAV is not an active explainer"))


@pytest.fixture
def generate_image():

    def _generate(width, height, alpha=False):
        channels = 4 if alpha else 3

        img = [channels * [min(255, v) for v in range(width)] for _ in range(height)]
        w = png.Writer(width, height, greyscale=False, alpha=alpha)

        f = io.BytesIO()
        w.write(f, img)
        f.seek(0)

        return f

    return _generate