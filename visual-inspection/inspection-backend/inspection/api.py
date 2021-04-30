from typing import Dict, Union, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, StrictBool, StrictFloat, StrictInt, ValidationError, validator
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY

from .config import settings as _settings
from .explainer.explain import EXPLAINERS, Explanation, explain
from .model.predict import Prediction, predict

api = APIRouter()


@api.post("/predict")
def predict_weather(file: UploadFile = File(...)) -> Prediction:
    return predict(file.file)


# TODO: Allow non-nested settings
class ExplanationRequest(BaseModel):
    method: str = _settings.default_explainer
    index_of_label_to_explain: int = 0
    settings: Dict[str, Dict[str, Union[StrictInt, StrictFloat, StrictBool,
                                        int, float, bool,
                                        str]]]

    class Config:
        extra = 'forbid'
        validate_all = True
        validate_assignment = True

    @validator("method")
    def method_must_be_available(cls, v):
        if v not in EXPLAINERS:
            raise ValueError(f"{v} is not an available explanation method")
        return v

#Nader We shoud add a top_index here to indey the top labels
@api.post("/explain")
def explain_classification(file: UploadFile = File(...),
                           method: Optional[str] = Form(None),
                           index_of_label_to_explain: Optional[int] = Form(None),
                           settings: Optional[str] = Form(None)) -> Explanation:
    if settings is not None:
        if method is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="If settings are given, method must be specified."
            )

    settings = settings or "{}"
    method = method or _settings.default_explainer

    try:
        request = ExplanationRequest.parse_raw('{"settings":' + settings + '}')
        request.method = method
        request.index_of_label_to_explain = index_of_label_to_explain
    except ValidationError as errors_out:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=errors_out.errors()
        )

    return explain(file.file, method=request.method,index_of_label_to_explain=request.index_of_label_to_explain , settings=request.settings)
