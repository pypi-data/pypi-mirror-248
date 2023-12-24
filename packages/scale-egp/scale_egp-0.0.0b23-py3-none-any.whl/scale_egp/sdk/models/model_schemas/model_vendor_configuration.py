from enum import Enum
from typing import Dict, List, Literal, Optional

from pydantic import Field

try:
    from egp_api_backend.server.api.utils.model_utils import BaseModel
except Exception:
    from pydantic import BaseModel

from .model_enums import ModelEndpointType, ModelVendor


class GPUType(str, Enum):
    # Supported GPU models according to
    # https://github.com/scaleapi/launch-python-client/blob/794089b9ed58330a7ecac02eb5060bcc4ae3d409/launch/client.py#L1470-L1471
    NVIDIA_TESLA_T4 = "nvidia-tesla-t4"
    NVIDIA_AMPERE_A10 = "nvidia-ampere-a10"
    NVIDIA_AMPERE_A100 = "nvidia-ampere-a100"
    NVIDIA_AMPERE_A100e = "nvidia-ampere-a100e"


# The fields in CreateModelBundleConfig(BaseModel) are based on the arguments to
# create_model_bundle_from_runnable_image_v2() in the Launch python client:
# https://github.com/scaleapi/launch-python-client/blob/794089b9ed58330a7ecac02eb5060bcc4ae3d409/launch/client.py#L668
# Differences between this class and the function arguments:
# * Separate fields for docker repository and image name.
# * Omitted fields: tag, healthcheck_route, predict_route, metadata - for these fields EGP user will need to
#   use the defaults provided by Launch.
#
class CreateModelBundleConfig(BaseModel):
    registry: str
    image: str
    tag: str
    command: List[str] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)
    readiness_initial_delay_seconds: int = Field(120)

    @property
    def full_repository_name(self):
        return "/".join([self.registry, self.image])


# The fields in CreateModelEndpointConfig are copied from the arguments of the Launch client's create_model_endpoint()
# https://github.com/scaleapi/launch-python-client/blob/794089b9ed58330a7ecac02eb5060bcc4ae3d409/launch/client.py#L1391
class CreateModelEndpointConfig(BaseModel):
    cpus: int = Field(3)
    memory: str = Field("8Gi")
    storage: str = Field("16Gi")
    gpus: int = Field(0)
    # By default, we create model endpoints with min_workers = 0 so unused model endpoints can be autoscaled down to
    # 0 workers, costing nothing.
    min_workers: int = Field(0)
    max_workers: int = Field(1)
    per_worker: int = Field(10)
    gpu_type: Optional[GPUType] = Field(None)
    endpoint_type: ModelEndpointType = Field(ModelEndpointType.ASYNC)
    high_priority: Optional[bool] = Field(False)


class LaunchVendorConfiguration(BaseModel):
    # this field is required for forward compatibility (other providers will have differend "vendor" fields)
    vendor: Literal[ModelVendor.LLMENGINE] = Field(ModelVendor.LLMENGINE)
    bundle_config: CreateModelBundleConfig
    endpoint_config: Optional[CreateModelEndpointConfig]


# Model vendor configuration only necessary for Launch models currently
ModelVendorConfiguration = LaunchVendorConfiguration
