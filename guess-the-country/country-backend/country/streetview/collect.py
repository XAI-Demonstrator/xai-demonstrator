import base64
import random
from typing import List, Optional

import httpx
from pydantic import BaseModel
from xaidemo.tracing import traced

from .polygon import generate_random
from .streetviewcity import get_cities, StreetviewCity


class Streetview(BaseModel):
    image: bytes
    class_label: str

# https://developers.google.com/maps/documentation/streetview
API_METADATA_URL = "https://maps.googleapis.com/maps/api/streetview/metadata"
API_STREETVIEW_URL = "https://maps.googleapis.com/maps/api/streetview"
DEFAULT_TIMEOUT = 10.0

MAX_METADATA_ATTEMPTS = 20

country_array: List[StreetviewCity] = get_cities()


def check_metadata_status(status: Optional[str]) -> bool:
    """
    Check if metadata status code is 200 or not. If not, return False or raise error
    https://developers.google.com/maps/documentation/streetview/metadata?hl=de#status-codes
    """
    if status is None:
        raise RuntimeError("StreetView metadata missing 'status' field")

    if status == "OK":
        return True

    raise_errors = {
        "REQUEST_DENIED": "Street View request denied — check GOOGLE_MAPS_API_TOKEN",
        # TODO: DISCUSS --> ZERO_RESULTS could also be a "retry-error" but all coordinates in streetview.py should deliver valid images?
        "ZERO_RESULTS": "Street View request returned zero results - no panorama found",
        "NOT_FOUND": "Street View request returned no results",
        "INVALID_REQUEST": "Street View request returned an invalid request - search parameters invalid or missing",

    }

    retry_errors = {
        "OVER_QUERY_LIMIT": "Street View request returned over a query limit - limit for this api reached",
        "UNKNOWN_ERROR": "Street View request returned an unknown error - server error"
    }

    if status in raise_errors:
        raise RuntimeError(raise_errors[status])
    elif status in retry_errors:
        print(f"WARN: {retry_errors[status]} - Trying again")  # TODO: Check if we use logging

    return False


@traced
async def get_streetview(API_KEY: str) -> Streetview:
    nominated_country = random.randrange(len(country_array))
    poly = country_array[nominated_country].polygon

    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        attempts = 0

        while attempts < MAX_METADATA_ATTEMPTS:
            coord = generate_random(poly)
            location_str = f"{coord[0][1]},{coord[0][0]}"

            meta_params = {
                "key": API_KEY,
                "location": location_str,
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
            if check_metadata_status(status):
                break

            else:
                attempts += 1
                print(f"WARN: Retry - attempt {attempts}/{MAX_METADATA_ATTEMPTS}")  # TODO: Check if we use logging
                continue

        else:
            raise RuntimeError(f"No StreetView panorama found after {MAX_METADATA_ATTEMPTS} attempts")

        img_params = {
            "key": API_KEY,
            "location": location_str,
            "size": "640x640"
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
