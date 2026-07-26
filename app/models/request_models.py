from pydantic import BaseModel, Field, HttpUrl
from typing import Literal


class PromptRequest(BaseModel):

    prompt: str = Field(
        ...,
        min_length=1,
        description="Prompt for the LLM",
    )


class VideoRequest(BaseModel):

    source:Literal["youtube", "local"]


    value: str


class SummaryResult(BaseModel):
    title: str
    summary: str
    key_points: list[str]