import pathlib

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

__all__ = ["vue_frontend"]


def _return_if_exists(path):
    if path.exists():
        return FileResponse(path)
    else:
        raise HTTPException(status_code=404)


def vue_frontend(main___file__: str) -> APIRouter:
    router = APIRouter()

    @router.get("/")
    def get_frontend():
        return _return_if_exists(pathlib.Path(main___file__).parent / "static" / "index.html")

    @router.get("/favicon.ico")
    def get_favicon():
        return _return_if_exists(pathlib.Path(main___file__).parent / "static" / "favicon.ico")

    @router.get("/{folder}/{fname}")
    def get_static(folder: str, fname: str):
        return _return_if_exists(pathlib.Path(main___file__).parent / "static" / folder / fname)

    return router
