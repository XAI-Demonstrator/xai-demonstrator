import io

import png
import pytest


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

