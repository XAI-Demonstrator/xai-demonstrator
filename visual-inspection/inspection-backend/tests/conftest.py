import io

import png
import pytest


@pytest.fixture
def dummy_image():
    img = [3 * [v for v in range(240)] for _ in range(240)]
    w = png.Writer(240, 240, greyscale=False)

    f = io.BytesIO()
    w.write(f, img)
    f.seek(0)

    yield f

    f.close()
