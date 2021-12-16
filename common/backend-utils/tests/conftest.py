import aioresponses
import pytest


@pytest.fixture
def aiomock():
    with aioresponses.aioresponses() as m:
        yield m
