from pydantic import BaseModel, Field, HttpUrl


class PromptRequest(BaseModel):

    prompt: str = Field(
        ...,
        min_length=1,
        description="Prompt for the LLM",
    )


class YoutubeRequest(BaseModel):

    youtube_url: HttpUrl


class SummaryResult(BaseModel):
    title: str
    summary: str
    key_points: list[str]