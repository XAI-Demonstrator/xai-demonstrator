import pytest
from shapely import Polygon, Point

from country.streetview import client


ULM = [
    (48.4389227572347, 9.938331354351565),
    (48.36518684941598, 9.881168116128428),
    (48.401099445347256, 10.10432790396745),
    (48.44712169035685, 9.990344750927209),
]

# for some reason, the coordinates within the backend
# are stored as (lon, lat) instead of (lat, lon)
REVERSED_ULM = [(lon, lat) for lat, lon in ULM]


@pytest.mark.streetview
@pytest.mark.anyio
async def test_that_a_random_streetview_image_is_returned(streetview_api_key):
    await client.get_random_streetview_image(api_key=streetview_api_key)


def test_that_point_within_a_polygon_is_found():
    polygon = Polygon([(0, 0), (0, 1), (1, 0), (1, 1)])

    x, y = client.get_random_coordinate_within(polygon)

    assert 0 <= x <= 1
    assert 0 <= y <= 1


@pytest.mark.streetview
@pytest.mark.anyio
async def test_that_streetview_location_is_found(streetview_api_key):
    ulm = Polygon(REVERSED_ULM)

    lat, lon = await client.get_streetview_location_within(
        ulm, api_key=streetview_api_key
    )

    assert ulm.contains(Point(lon, lat))


@pytest.mark.streetview
@pytest.mark.anyio
async def test_that_streetview_image_is_found(streetview_api_key):
    await client.get_streetview_image_at(
        lat=48.42589367593841, lon=9.956390447614666, api_key=streetview_api_key
    )
