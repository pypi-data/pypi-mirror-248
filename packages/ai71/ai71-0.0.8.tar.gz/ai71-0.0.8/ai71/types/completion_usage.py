import pydantic


class CompletionUsage(pydantic.BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
