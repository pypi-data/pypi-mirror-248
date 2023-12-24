from enum import Enum


class ModelState(str, Enum):
    ENABLED = "ENABLED"
    PENDING = "PENDING"
    DISABLED = "DISABLED"


class ModelVendor(str, Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    ANTHROPIC = "ANTHROPIC"
    LLMENGINE = "LLMENGINE"
    OTHER = "OTHER"


class ModelEndpointType(str, Enum):
    SYNC = "SYNC"
    ASYNC = "ASYNC"
    STREAMING = "STREAMING"
    BATCH = "BATCH"


class ModelType(str, Enum):
    COMPLETION = "COMPLETION"
    CHAT_COMPLETION = "CHAT_COMPLETION"
    AGENT = "AGENT"
    EMBEDDING = "EMBEDDING"
    RERANKING = "RERANKING"
