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


@router.get("/css/{fname}")
def style(fname):
    return FileResponse(pathlib.Path(__file__).parent.parent / "static" / "css" / fname)


@router.get("/js/{fname}")
def script(fname):
    return FileResponse(pathlib.Path(__file__).parent.parent / "static" / "js" / fname)


@router.get("/img/{fname}")
def script(fname):
    return FileResponse(pathlib.Path(__file__).parent.parent / "static" / "img" / fname)
