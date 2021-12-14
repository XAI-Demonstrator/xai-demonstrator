import pytest
import aiohttp


from fastapi import UploadFile

@pytest.mark.asyncio
async def test_that_json_calls_work(proxy):
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy + "/json", json={"hello": "world"}) as response:
            assert response.status == 200


@pytest.mark.asyncio
async def test_that_form_calls_work(proxy):
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy + "/form", data={"hello": "world"}) as response:
            assert response.status == 200


@pytest.mark.asyncio
async def test_that_files_can_be_sent(proxy, generate_image):
    async with aiohttp.ClientSession() as session:
        async with session.post(proxy + "/form", data={"image": generate_image(100, 100)}) as response:
            assert response.status == 200
