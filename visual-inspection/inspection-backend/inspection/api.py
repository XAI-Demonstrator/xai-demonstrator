from typing import Any, Dict, Union

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, StrictFloat, StrictInt, StrictBool, ValidationError, validator
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .config import settings as _settings
from .explainer.explain import EXPLAINERS, Explanation, explain
from .model.predict import Prediction, predict

api = APIRouter()


@api.post("/predict")
def predict_weather(file: UploadFile = File(...)) -> Prediction:
    return predict(file.file)


class ExplanationSettings(BaseModel):
    settings: Dict[str, Dict[str, Union[StrictInt, StrictFloat, StrictBool,
                                        int, float, bool,
                                        str]]]


class ExplanationRequest(BaseModel):
    method: str = _settings.default_explainer
    settings: Dict[str, Dict[str, Union[int, float, bool, str]]]

    @validator("method")
    def method_must_be_available(cls, v):
        if v not in EXPLAINERS:
            raise ValueError(f"{v} is not an available explanation method")
        return v


@api.post("/explain")
def explain_classification(file: UploadFile = File(...),
                           method: str = Form(_settings.default_explainer),
                           settings: str = Form("{{}}")) -> Explanation:

    try:
        parsed_settings = ExplanationSettings.parse_raw('{"settings":' + settings + '}')
    except ValidationError as errors_out:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=errors_out.errors()
        )

    try:
        request = ExplanationRequest(method=method,
                                     settings=parsed_settings.settings)
    except ValidationError as errors_out:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=errors_out.errors()
        )

    return explain(file.file, method=request.method, settings=request.settings)
