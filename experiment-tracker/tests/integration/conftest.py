import io

import png
import pytest
from pydantic import BaseSettings


class TestSettings(BaseSettings):
    COUCHDB_URL: str
    COLLECTOR_URL: str
    PROXY_URL: str
    SERVICE_URL: str


settings = TestSettings()


@pytest.fixture
def couchdb():
    return settings.COUCHDB_URL


@pytest.fixture
def collector():
    return settings.COLLECTOR_URL


@pytest.fixture
def proxy():
    return settings.PROXY_URL


@pytest.fixture
def service():
    return settings.SERVICE_URL


@pytest.fixture
def generate_image():

    def _generate(width, height):
        img = [3 * [min(255, v) for v in range(width)] for _ in range(height)]
        w = png.Writer(width, height, greyscale=False, alpha=False)

        f = io.BytesIO()
        w.write(f, img)
        f.seek(0)

        return f

    return _generate
