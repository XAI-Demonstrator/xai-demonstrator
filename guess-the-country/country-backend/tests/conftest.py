import io

import png
import pytest
import base64


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


def gernerate_base64():

    def _generate(width, height, alpha=False):
        channels = 4 if alpha else 3

        img = [channels * [min(255, v) for v in range(width)] for _ in range(height)]
        w = png.Writer(width, height, greyscale=False, alpha=alpha)

        f = io.BytesIO()
        w.write(f, img)
        encoded_image_string = base64.b64encode(f.seek(0))
        encoded_bytes = bytes("data:image/png;base64,",
                              encoding="utf-8") + encoded_image_string
        return encoded_bytes

    return _generate