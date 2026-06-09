from typing import Dict, Union, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, StrictBool, StrictFloat, StrictInt, ValidationError, field_validator
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY

from .config import settings as _settings
from .explainer.explain import EXPLAINERS, Explanation, explain
from .model.predict import Prediction, predict

api = APIRouter()


@api.post("/predict")
def predict_object(file: UploadFile = File(...),
                   language: Optional[str] = Form(None),
                   model_id: Optional[str] = Form(None)) -> Prediction:
    model_id = model_id or _settings.default_model
    return predict(image_file=file.file, language=language, model_id=model_id)


# TODO: Allow non-nested settings
class ExplanationRequest(BaseModel):
    method: str = _settings.default_explainer
    model_id: str = _settings.default_model
    settings: Dict[str, Dict[str, Union[int, float, bool, str]]]

    class Config:
        extra = 'forbid'

    @field_validator("settings", mode="before")
    @classmethod
    def coerce_settings_values(cls, value: Dict[str, Dict[str, object]]):
        coerced = {}
        for section, params in value.items():
            new_params = {}
            for key, v in params.items():
                if isinstance(v, str):
                    if v.lower() == "true":
                        new_v = True
                    elif v.lower() == "false":
                        new_v = False
                    else:
                        try:
                            new_v = int(v)
                        except ValueError:
                            try:
                                new_v = float(v)
                            except ValueError:
                                new_v = v
                else:
                    new_v = v
                new_params[key] = new_v
            coerced[section] = new_params
        return coerced

    @field_validator("method")
    @classmethod
    def method_must_be_available(cls, v):
        if v not in EXPLAINERS:
            raise ValueError(f"{v} is not an available explanation method")
        return v


@api.post("/explain")
def explain_classification(file: UploadFile = File(...),
                           method: Optional[str] = Form(None),
                           model_id: Optional[str] = Form(None),
                           settings: Optional[str] = Form(None)) -> Explanation:
    if settings is not None:
        if method is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="If settings are given, method must be specified."
            )

    settings = settings or "{}"

    try:
        request = ExplanationRequest.model_validate_json('{"settings":' + settings + '}')
    except ValidationError as errors_out:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=errors_out.errors()
        )
    else:
        request.method = method or request.method
        request.model_id = model_id or request.model_id

        if request.method not in EXPLAINERS:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"{request.method} is not an available explanation method",
            )

    return explain(file.file, model_id=request.model_id, method=request.method, settings=request.settings)
