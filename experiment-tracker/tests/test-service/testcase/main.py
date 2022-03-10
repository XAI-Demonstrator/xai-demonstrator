from fastapi import FastAPI, Request, UploadFile, File
from pydantic import BaseModel
from xaidemo import tracing, tracking

tracing.set_up()

app = FastAPI()
tracking.instrument_app(app)


class TestResponse(BaseModel):
    received: str
    num_of_keys: int


@app.post("/json")
async def handle_json(request: Request) -> TestResponse:
    return TestResponse(received="Request with JSON payload.",
                        num_of_keys=len(await request.json()))


@app.post("/form")
async def handle_form(request: Request) -> TestResponse:
    return TestResponse(received="Request with FormData payload.",
                        num_of_keys=len(await request.form()))


@app.post("/file")
async def handle_file(file: UploadFile = File(...)) -> TestResponse:
    return TestResponse(received=f"Request with file {file.filename}.",
                        num_of_keys=1)


@app.post("/json_with_record")
async def handle_json(request: Request) -> TestResponse:
    tracking.record_data("backend", {"msg": "hello world!"})
    return TestResponse(received="Request with JSON payload.",
                        num_of_keys=len(await request.json()))


@app.get("/{some_id}")
async def handle_resource_request(some_id: str):
    tracking.record_data("backend", {"msg": some_id})
    return TestResponse(received=f"Received GET request at {some_id}.",
                        num_of_keys=0)


tracing.instrument_app(app)
