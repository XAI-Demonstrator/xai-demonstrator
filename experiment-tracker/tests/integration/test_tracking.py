import pytest
import aiohttp
import asyncio


@pytest.mark.asyncio
async def test_that_json_calls_work(proxy):
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy + "/json", json={"hello": "world"}) as response:
            assert response.status == 200
            msg = await response.json()
            assert msg["num_of_keys"] == 1


@pytest.mark.asyncio
async def test_that_form_calls_work(proxy):
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy + "/form", data={"hello": "world"}) as response:
            assert response.status == 200
            msg = await response.json()
            assert msg["num_of_keys"] == 1


@pytest.mark.asyncio
async def test_that_files_can_be_sent(proxy, generate_image):
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy + "/form", data={"image": generate_image(100, 100)}) as response:
            assert response.status == 200
            msg = await response.json()
            assert msg["num_of_keys"] == 1


@pytest.mark.asyncio
async def test_that_request_is_recorded(proxy, collector):
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy + "/json", json={"find": "me"}) as response:
            assert response.status == 200

        # Wait for the collector to receive the data
        await asyncio.sleep(10)

        async with session.get(collector + "/dump") as response:
            assert response.status == 200
            dump = await response.json()

        for record in dump["records"]:
            if "find" in record["data"]["tracked"]["data"]["request"]["decoded"]:
                break
        else:
            raise AssertionError("Did not find entry")

        id_ = record["id"]

        async with session.get(collector + f"/get/{id_}") as response:
            assert response.status == 200
            single_record = await response.json()

        assert record == single_record


@pytest.mark.asyncio
async def test_that_one_call_yields_one_record(proxy, collector):
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy + "/json_with_record", json={"find": "me i'm special"}) as response:
            assert response.status == 200

        # Wait for the collector to receive the data
        await asyncio.sleep(10)

        async with session.get(collector + "/dump") as response:
            assert response.status == 200
            dump = await response.json()

        for record in dump["records"]:
            if "backend" in record["data"]:
                break
        else:
            raise AssertionError("Did not find entry")

        assert "tracked" in record["data"]
        assert record["data"]["tracked"]["data"]["find"] == "me i'm special"
