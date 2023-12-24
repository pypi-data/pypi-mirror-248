# copied from  from packages/egp-api-backend/egp_api_backend/server/api/models/egp_models.py
from typing import Optional

from pydantic import BaseModel, Extra

from .parameter_schema import ParameterBindings


class BaseModelRequest(BaseModel):
    model_request_parameters: Optional[ParameterBindings]

    class Config:
        extra = Extra.forbid


class BaseModelResponse(BaseModel):
    class Config:
        extra = Extra.forbid
