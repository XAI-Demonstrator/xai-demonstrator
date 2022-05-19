import io
from json import JSONDecodeError
from typing import Dict, Any

import aiohttp
from fastapi import FastAPI, Response, Path, Request, BackgroundTasks, HTTPException
from multipart.multipart import parse_options_header
from starlette.datastructures import UploadFile
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from xaidemo import tracing, http_client
from xaidemo.tracking.record import send_record

from .config import settings
from .record import RequestData, ResponseData, TrackedData, prepare_record

tracing.set_up()

app = FastAPI()
http_client.set_up(app)

backend_timeout = aiohttp.ClientTimeout(settings.backend_timeout)


@app.post("/{endpoint}")
@app.get("/{endpoint}")
async def proxy(request: Request,
                background_tasks: BackgroundTasks,
                endpoint: str = Path(...)) -> Response:
    # NOTE: We need to first consume the stream once and cache the body
    # The form parsing calls request.stream() which does not store the result in request._body,
    # but checks whether request._body exists and returns it instead of attempting to consume
    # the stream again
    body = await request.body()

    content_type = request.headers.get("Content-Type", None)
    if content_type is not None:
        content_type, _ = parse_options_header(content_type)
        msg = await parse_content(content_type, request)
        decoded_request = await decode_request(msg)
    else:
        msg = {}
        decoded_request = {}

    if "data" in msg:
        for key, value in msg["data"].items():
            if isinstance(value, UploadFile):
                value.file.seek(0)
                msg["data"][key] = io.BytesIO(value.file.read())

    async with http_client.AioHttpClientSession() as session:
        if request.method == "POST":
            call_method = session.post
        elif request.method == "GET":
            call_method = session.get
        else:
            raise NotImplementedError

        async with call_method(settings.backend_url + "/" + endpoint,
                               timeout=backend_timeout,
                               **msg) as proxy_response:
            response = Response()
            response.status_code = proxy_response.status
            response.init_headers(proxy_response.headers)
            response.body = await proxy_response.read()
            decoded_response = await decode_response(response, proxy_response)

    if response.headers["content-type"] == "application/json":
        tracked_data = TrackedData(request=RequestData(raw=body.hex(' ', 4),
                                                       content_type=content_type,
                                                       decoded=decoded_request),
                                   response=ResponseData(raw=response.body.hex(' ', 4),
                                                         decoded=decoded_response,
                                                         status_code=response.status_code))

        partial_record_request = prepare_record(endpoint=endpoint, key="tracked", value=tracked_data)
        background_tasks.add_task(send_record, partial_record_request)

    return response


async def parse_content(content_type: bytes, request: Request) -> Dict[str, Any]:
    if content_type == b"application/json":
        try:
            msg = {"json": await request.json()}
        except (JSONDecodeError, TypeError) as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail=f"Failed to decode JSON: {e}")
    elif content_type in [b"multipart/form-data", b"application/x-www-form-urlencoded"]:
        try:
            formdata = await request.form()
        except Exception as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail=f"Failed to decode Form data: {e}")
        else:
            msg = {"data": dict(formdata.items())}
    else:
        raise HTTPException(status_code=HTTP_406_NOT_ACCEPTABLE,
                            detail="The experiment proxy only accepts application/json, multipart/form-data, "
                                   "and application/x-www-form-urlencoded.")
    return msg


async def decode_request(msg: Dict[str, Any]) -> Dict[str, Any]:
    decoded_request = {}
    _request_payload = list(msg.values())[0]
    for key, value in _request_payload.items():
        if isinstance(value, UploadFile):
            value.file.seek(0)
            decoded_request[key] = value.file.read().hex(' ', 4)
        else:
            decoded_request[key] = value
    return decoded_request


async def decode_response(response: Response, proxy_response: aiohttp.ClientResponse) -> Dict[str, Any]:
    if response.body:
        try:
            decoded_response = await proxy_response.json()
        except (JSONDecodeError, TypeError):
            raise HTTPException(status_code=HTTP_406_NOT_ACCEPTABLE,
                                detail="Could not parse JSON response.")
    else:
        decoded_response = {}
    return decoded_response


tracing.instrument_app(app)
