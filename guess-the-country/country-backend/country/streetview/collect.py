import base64
import random
from typing import List

import httpx
from pydantic import BaseModel
from xaidemo.http_client import AioHttpClientSession
from xaidemo.tracing import traced

from .polygon import generate_random
from .streetviewcity import get_cities, StreetviewCity


class Streetview(BaseModel):
    image: bytes
    class_label: str

API_METADATA_URL = "https://maps.googleapis.com/maps/api/streetview/metadata"
API_STREETVIEW_URL = "https://maps.googleapis.com/maps/api/streetview"
DEFAULT_TIMEOUT = 10.0

country_array: List[StreetviewCity] = get_cities()


@traced
async def get_streetview(API_KEY: str) -> Streetview:
    nominated_country = random.randrange(len(country_array))
    poly = country_array[nominated_country].polygon

    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        while True:
            coord = generate_random(poly)
            lng, lat = coord[0][0], coord[0][1]
            loc = f"{lat},{lng}"

            meta_params = {
                "key": API_KEY,
                "location": loc,
                "source": "outdoor",
                "return_error_code": "true",
            }

            try:
                meta_resp = await client.get(API_METADATA_URL, params=meta_params)
                meta_resp.raise_for_status()
                meta = meta_resp.json()
            except httpx.RequestError as e:
                raise RuntimeError("StreetView metadata network error") from e
            except ValueError as e:
                raise RuntimeError("StreetView metadata returned invalid JSON") from e

            status = meta.get("status")
            if status == "OK":
                break
            if status == "REQUEST_DENIED":
                raise RuntimeError("Street View request denied — check GOOGLE_MAPS_API_TOKEN")


        img_params = {
            "key": API_KEY,
            "location": loc,
            "size": "640x640",
            "source": "outdoor",
        }

        try:
            img_resp = await client.get(API_STREETVIEW_URL, params=img_params)
            img_resp.raise_for_status()
            contents = img_resp.content
            if not contents:
                raise RuntimeError("Empty StreetView image")
        except httpx.RequestError as e:
            raise RuntimeError("Failed to fetch StreetView image") from e

    encoded_bytes = b"data:image/png;base64," + base64.b64encode(contents)
    return Streetview(image=encoded_bytes, class_label=country_array[nominated_country].city)
