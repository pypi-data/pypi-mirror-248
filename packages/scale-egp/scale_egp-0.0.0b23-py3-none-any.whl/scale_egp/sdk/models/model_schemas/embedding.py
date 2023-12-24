from typing import List, Tuple

from .common import BaseModelRequest, BaseModelResponse


class EmbeddingRequest(BaseModelRequest):
    texts: List[str]


class EmbeddingResponse(BaseModelResponse):
    # List of text, embedding pairs, eg: [("text to get embedding for", [1.0, 1.05, 2.07, ...]), ...]
    embeddings: List[Tuple[str, List[float]]]
