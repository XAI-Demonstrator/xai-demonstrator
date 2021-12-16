import aiohttp
import pytest


@pytest.mark.asyncio
async def test_that_test_service_is_available(service):
    async with aiohttp.ClientSession() as session:
        async with session.post(service + "/json_with_record", json={"find": "me"}) as response:
            assert response.status == 200

        async with session.post(service + "/json", json={"find": "me"}) as response:
            assert response.status == 200

        async with session.post(service + "/form", data={"find": "me"}) as response:
            assert response.status == 200


@pytest.mark.asyncio
async def test_that_proxy_is_available(proxy):
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy + "/json", json={"find": "me"}) as response:
            assert response.status == 200


@pytest.mark.asyncio
async def test_that_collector_is_available(collector):
    async with aiohttp.ClientSession() as session:
        async with session.get(collector + "/dump") as response:
            assert response.status == 200
