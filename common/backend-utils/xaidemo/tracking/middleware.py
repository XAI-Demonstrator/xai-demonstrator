from typing import Callable, Awaitable

from fastapi import BackgroundTasks
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .record import get_record_id, TaskMemory, send_record


class ExperimentTrackerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)
        if response.background is None:
            response.background = BackgroundTasks()

        record_id = get_record_id()

        if isinstance(response.background, BackgroundTasks):
            for task in TaskMemory.get_tasks_and_erase_memory(record_id):
                response.background.add_task(send_record, task)
        else:
            raise ValueError("Non-FastAPI background tasks.")

        return response
