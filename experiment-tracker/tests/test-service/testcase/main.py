from fastapi import FastAPI, Request
from pydantic import BaseModel
from xaidemo import tracing

tracing.set_up()

app = FastAPI()


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

tracing.instrument_app(app)
