from fastapi import FastAPI, Request
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


@app.post("/json_with_record")
async def handle_json(request: Request) -> TestResponse:
    tracking.record_data("backend", {"msg": "hello world!"})
    return TestResponse(received="Request with JSON payload.",
                        num_of_keys=len(await request.json()))


tracing.instrument_app(app)
