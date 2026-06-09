import base64

import respx
import httpx
import pytest

from country.streetview import collect

@pytest.mark.asyncio
@respx.mock
async def test_get_streetview_with_mock(monkeypatch):
    meta_url = collect.API_METADATA_URL
    img_url = collect.API_STREETVIEW_URL

    respx.get(meta_url).mock(return_value=httpx.Response(200, json={"status": "OK"}))
    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    respx.get(img_url).mock(return_value=httpx.Response(200, content=png_bytes))

    sv = await collect.get_streetview("DUMMY_KEY")

    assert isinstance(sv.image, (bytes, bytearray))
    assert sv.image.startswith(b"data:image/png;base64,")
    decoded = base64.b64decode(sv.image.split(b",", 1)[1])
    assert decoded.startswith(b"\x89PNG")
    assert isinstance(sv.class_label, str)



@pytest.mark.asyncio
@respx.mock
async def test_get_streetview_retries_then_succeeds(monkeypatch):
    meta_url = collect.API_METADATA_URL
    img_url = collect.API_STREETVIEW_URL

    meta_route = respx.get(meta_url).mock(side_effect=[
        httpx.Response(200, json={"status": "UNKNOWN_ERROR"}),
        httpx.Response(200, json={"status": "UNKNOWN_ERROR"}),
        httpx.Response(200, json={"status": "OK"}),
    ])

    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    respx.get(img_url).mock(return_value=httpx.Response(200, content=png_bytes))

    sv = await collect.get_streetview("DUMMY_KEY")

    assert isinstance(sv.image, (bytes, bytearray))
    assert sv.image.startswith(b"data:image/png;base64,")
    decoded = base64.b64decode(sv.image.split(b",", 1)[1])
    assert decoded.startswith(b"\x89PNG")
    assert isinstance(sv.class_label, str)
    assert meta_route.call_count == 3


@pytest.mark.asyncio
@respx.mock
async def test_get_streetview_exhausts_retries_then_raises(monkeypatch):
    meta_url = collect.API_METADATA_URL
    meta_route = respx.get(meta_url).mock(return_value=httpx.Response(200, json={"status": "UNKNOWN_ERROR"}))

    with pytest.raises(RuntimeError, match="No StreetView panorama found after"):
        await collect.get_streetview("DUMMY_KEY")

    assert meta_route.call_count == collect.MAX_METADATA_ATTEMPTS
