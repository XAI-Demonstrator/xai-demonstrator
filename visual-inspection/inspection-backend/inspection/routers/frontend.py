import pathlib

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/")
def frontend():
    return FileResponse(pathlib.Path(__file__).parent.parent / "static" / "index.html")


@router.get("/favicon.ico")
def favicon():
    return FileResponse(pathlib.Path(__file__).parent.parent / "static" / "favicon.ico")


@router.get("/{folder}/{fname}")
def static(folder, fname):
    return FileResponse(pathlib.Path(__file__).parent.parent / "static" / folder / fname)
