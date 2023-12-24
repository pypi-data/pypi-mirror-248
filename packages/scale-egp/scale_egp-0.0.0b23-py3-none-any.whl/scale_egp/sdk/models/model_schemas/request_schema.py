from typing import Optional, Type

from pydantic import create_model

from .common import BaseModelRequest, BaseModelResponse
from .model_enums import ModelType
from .model_schemas import MODEL_SCHEMAS
from .parameter_schema import ParameterSchema, ParameterSchemaModelConfig, parameter_schema_to_model


def get_full_request_schema(
    model_type: ModelType,
    model_request_parameter_schema: Optional[ParameterSchema] = None,
) -> Type[BaseModelRequest]:
    # dynamically construct Pydantic model which fully describes the model request schema
    # including the model_request_parameters field if it is used by the model.
    request_schema = create_model(
        MODEL_SCHEMAS[model_type][0].__name__,
        __config__=ParameterSchemaModelConfig,
    )
    # copy over all fields except model_request_parameters
    fields = {
        field_name: field_info
        for field_name, field_info in MODEL_SCHEMAS[model_type][0].__fields__.items()
        if field_name != "model_request_parameters"
    }
    if model_request_parameter_schema and len(model_request_parameter_schema.parameters) > 0:
        request_parameter_schema_cls = parameter_schema_to_model(
            "model_request_parameter_schema",
            model_request_parameter_schema,
        )
        fields["model_request_parameters"] = (request_parameter_schema_cls, ...)
    else:
        # permit an empty model_request_parameters to be sent since pydantic will send it automatically
        fields["model_request_parameters"] = BaseModelRequest.__fields__["model_request_parameters"]

    request_schema.__fields__ = fields
    return request_schema


def get_response_schema(model_type: ModelType) -> Type[BaseModelResponse]:
    return MODEL_SCHEMAS[model_type][1]
