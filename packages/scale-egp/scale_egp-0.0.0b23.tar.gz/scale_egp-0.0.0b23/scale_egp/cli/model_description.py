import json
from typing import Any, Callable, Dict, Literal, Optional, Type, Union

from pydantic import BaseModel
from scale_egp.cli.formatter import Markdownable
from scale_egp.sdk.models.model_api_models import ModelAlias, ModelTemplate
from scale_egp.sdk.models.model_schemas.model_enums import ModelVendor
from scale_egp.sdk.models.model_schemas.request_schema import get_full_request_schema
from scale_egp.sdk.models.model_schemas.model_schemas import MODEL_SCHEMAS
from scale_egp.sdk.models.model_schemas.parameter_schema import parameter_schema_to_model


class ModelDescription(BaseModel, Markdownable):
    model_instance: ModelAlias
    model_template: ModelTemplate

    def _get_request_schema(self) -> Dict[str, Any]:
        return get_full_request_schema(
            self.model_template.model_type,
            self.model_template.model_request_parameters_schema,
        ).schema()

    def _get_description_dict(self) -> Dict[str, Any]:
        return {
            "model_instance": json.loads(self.model_instance.json()),
            "model_template": json.loads(self.model_template.json()),
        }

    def to_markdown(self) -> str:
        return (
            f"# {self.model_instance.name} (id: {self.model_instance.id})\n"
            f"\n"
            f"*type*: {self.model_template.model_type.value}\n"
            f"*status*: {self.model_instance.status}\n"
            f"*vendor*: {(self.model_instance.model_vendor or ModelVendor.LLMENGINE).value}\n"
            f"\n"
            f"{self.model_instance.description or ''}\n"
            f"## Model request schema\n"
            f"```\n"
            f"{json.dumps(self.model_instance.request_schema, indent=2)}\n"
            f"```\n"
            f"## Model response schema\n"
            f"```\n"
            f"{json.dumps(self.model_instance.response_schema, indent=2)}\n"
            f"```\n"
        )

    def json(self, **dumps_kwargs: Any) -> str:
        return json.dumps(self._get_description_dict(), **dumps_kwargs)
