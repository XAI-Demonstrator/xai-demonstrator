import base64
import random
from typing import Tuple

from fastapi import HTTPException
from pydantic import BaseModel
from shapely.geometry import Point, Polygon
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from xaidemo.http_client import AioHttpClientSession, aiohttp
from xaidemo.tracing import traced

from .coordinates import CITY_BOUNDARIES
from ..config import settings


class StreetViewImage(BaseModel):
    image: bytes
    city: str
    country: str


# 25,000 image requests per 24 hours
# See https://developers.google.com/maps/documentation/streetview/
STREETVIEW_API_URL = f"https://maps.googleapis.com/maps/api/streetview?size={settings.streetview_image_size}x{settings.streetview_image_size}&sensor=false&source=outdoor"
STREETVIEW_METADATA_URL = "https://maps.googleapis.com/maps/api/streetview/metadata?source=outdoor"  # Not billed


@traced
async def get_random_streetview_image(
    api_key: str = settings.streetview_static_api_token,
) -> StreetViewImage:
    city_idx = random.randint(0, 3)
    city_label = CITY_BOUNDARIES[city_idx]["city"]
    country_label = CITY_BOUNDARIES[city_idx]["country"]
    city_boundary = CITY_BOUNDARIES[city_idx]["polygon"]

    lat, lon = await get_streetview_location_within(
        polygon=city_boundary, api_key=api_key
    )

    encoded_image = await get_streetview_image_at(lat=lat, lon=lon, api_key=api_key)

    return StreetViewImage(image=encoded_image, city=city_label, country=country_label)


@traced
def get_random_coordinate_within(polygon: Polygon) -> Tuple[int, int]:
    """Find a random point within the coordinate polygon."""

    min_x, min_y, max_x, max_y = polygon.bounds

    while True:
        pnt = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if polygon.contains(pnt):
            break

    return pnt.y, pnt.x


@traced
async def get_streetview_location_within(
    polygon: Polygon, api_key: str = settings.streetview_static_api_token
) -> Tuple[int, int]:
    """Find a location within the coordinate polygon where a StreetView image is available."""

    async with AioHttpClientSession() as session:
        for i in range(settings.streetview_max_retries):
            lat, lon = get_random_coordinate_within(polygon=polygon)

            metadata_url = (
                f"{STREETVIEW_METADATA_URL}&key={api_key}&location={lat},{lon}"
            )

            try:
                async with session.get(metadata_url) as response:
                    json_body = await response.json()
            except aiohttp.client.ClientError:
                raise HTTPException(
                    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Call to Google StreetView Metadata API failed.",
                )
            else:
                status = json_body["status"]
                if status == "REQUEST_DENIED":
                    raise HTTPException(
                        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Request to Google StreetView Metadata API was denied. "
                        "Please ensure that the environment variable STREETVIEW_STATIC_API_TOKEN "
                        "is set to a valid API token.",
                    )
                if status == "OK":
                    return lat, lon


@traced
async def get_streetview_image_at(
    lat: int, lon: int, api_key: str = settings.streetview_static_api_token
) -> bytes:
    image_url = f"{STREETVIEW_API_URL}&key={api_key}&location={lat},{lon}"

    async with AioHttpClientSession() as session:
        try:
            async with session.get(image_url) as response:
                content = await response.read()
        except aiohttp.client.ClientError:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Call to Google StreetView API failed.",
            )
        else:
            encoded_image = bytes(
                "data:image/png;base64,", encoding="utf-8"
            ) + base64.b64encode(content)

            return encoded_image
