from typing import Dict
from fastapi import FastAPI, UploadFile, Form, File

from .routers import frontend

app = FastAPI()
app.include_router(frontend.router)


@app.post("/predict")
def predict(file: UploadFile = File(...)):
    return file.filename


@app.post("/explain")
def explain(file: UploadFile = File(...),
            method: str = Form(...),
            settings: Dict = Form(...)):
    return file.filename
