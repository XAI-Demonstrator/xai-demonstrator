from json import JSONDecodeError

import aiohttp
from fastapi import FastAPI, Response, Path, Request, BackgroundTasks, HTTPException
from multipart.multipart import parse_options_header
from opentelemetry import trace
from opentelemetry.instrumentation.aiohttp_client import (
    AioHttpClientInstrumentor
)
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from starlette.datastructures import UploadFile
from xaidemo import tracing

from .config import settings
from .http_client import AioHttpClientSession
from .record import RequestData, ResponseData, TrackedData, record_data

tracing.set_up()
AioHttpClientInstrumentor().instrument()


async def on_shutdown():
    await AioHttpClientSession.close_client_session()


app = FastAPI(on_shutdown=[on_shutdown])

backend_timeout = aiohttp.ClientTimeout(settings.backend_timeout)


@app.post("/{endpoint}")
async def proxy(request: Request,
                response: Response,
                background_tasks: BackgroundTasks,
                endpoint: str = Path(...)):
    # NOTE: We need to first consume the stream once and cache the body
    # The form parsing calls request.stream() which does not store the result in request._body,
    # but checks whether request._body exists and returns it instead of attempting to consume
    # the stream again
    body = await request.body()

    content_type = request.headers.get("Content-Type", None)

    if content_type:
        content_type, _ = parse_options_header(content_type)

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
    elif content_type is None:
        msg = {}
    else:
        raise HTTPException(status_code=HTTP_406_NOT_ACCEPTABLE,
                            detail="The experiment proxy only accepts application/json, multipart/form-data, "
                                   "and application/x-www-form-urlencoded.")

    async with AioHttpClientSession() as session:
        async with session.post(settings.backend_url + "/" + endpoint,
                                timeout=backend_timeout,
                                **msg) as proxy_response:
            response.status_code = proxy_response.status
            response.init_headers(proxy_response.headers)
            response.body = await proxy_response.read()
            if response.body:
                try:
                    decoded_response = await proxy_response.json()
                except (JSONDecodeError, TypeError):
                    raise HTTPException(status_code=HTTP_406_NOT_ACCEPTABLE,
                                        detail="The experiment proxy can only handle JSON responses.")
            else:
                decoded_response = {}

    decoded_request = list(msg.values())[0] if content_type else {}
    for key, value in decoded_request.items():
        if isinstance(value, UploadFile):
            decoded_request[key] = value.file.read().hex(' ', 4)

    tracked_data = TrackedData(request=RequestData(raw=body.hex(' ', 4),
                                                   content_type=content_type,
                                                   decoded=decoded_request),
                               response=ResponseData(raw=response.body.hex(' ', 4),
                                                     decoded=decoded_response,
                                                     status_code=response.status_code))

    trace_id = trace.get_current_span().get_span_context().trace_id
    background_tasks.add_task(record_data, f"{trace_id:x}", endpoint, "tracked", tracked_data.dict())

    return response


tracing.instrument_app(app)
