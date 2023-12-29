from typing import Annotated, Literal, Optional, Sequence

import pydantic

from ..types.completion_usage import CompletionUsage
from ..types.finish_reason import FinishReason
from ..types.model import Model


class CreateCompletion(pydantic.BaseModel):
    prompt: str
    model: Model
    stream: bool = False
    max_tokens: int | None = None
    stop: Annotated[Sequence[str], pydantic.Field(str, max_length=8)] = []
    temperature: pydantic.NonNegativeFloat = 0.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    top_p: Annotated[float, pydantic.Field(float, gt=0.0, le=1.0)] = 1.0
    top_k: pydantic.PositiveInt | None = None


class Choice(pydantic.BaseModel):
    finish_reason: FinishReason
    index: int
    text: str


class Completion(pydantic.BaseModel):
    id: str
    choices: Sequence[Choice]
    created: int
    model: str
    object: Literal["completion"]
    system_fingerprint: Optional[str] = None
    usage: Optional[CompletionUsage] = None
