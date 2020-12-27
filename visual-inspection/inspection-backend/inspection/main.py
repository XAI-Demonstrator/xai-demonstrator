from fastapi import FastAPI

from .routers import frontend

app = FastAPI()
app.include_router(frontend.router)
