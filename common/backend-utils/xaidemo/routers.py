import pathlib

from fastapi import APIRouter
from fastapi.responses import FileResponse


def vue_frontend(main___file__: str) -> APIRouter:
    router = APIRouter()

    @router.get("/")
    def get_frontend():
        return FileResponse(pathlib.Path(main___file__).parent / "static" / "index.html")

    @router.get("/favicon.ico")
    def get_favicon():
        return FileResponse(pathlib.Path(main___file__).parent / "static" / "favicon.ico")

    @router.get("/{folder}/{fname}")
    def get_static(folder: str, fname: str):
        return FileResponse(pathlib.Path(main___file__).parent / "static" / folder / fname)

    return router
