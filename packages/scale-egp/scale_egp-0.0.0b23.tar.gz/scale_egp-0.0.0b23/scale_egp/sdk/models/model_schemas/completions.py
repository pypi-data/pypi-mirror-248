from typing import List, Tuple

from .completions_shared import CompletionBaseRequest, CompletionBaseResponse


class CompletionRequest(CompletionBaseRequest):
    prompts: List[str]


class CompletionResponse(CompletionBaseResponse):
    # List of prompt, completion pairs, eg: [("prompt", ["completion1", "completion2", ...]), ...]
    completions: List[Tuple[str, List[str]]]
