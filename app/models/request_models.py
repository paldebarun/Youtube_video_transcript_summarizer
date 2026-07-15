from pydantic import BaseModel, Field, HttpUrl


class PromptRequest(BaseModel):

    prompt: str = Field(
        ...,
        min_length=1,
        description="Prompt for the LLM",
    )


class YoutubeRequest(BaseModel):

    youtube_url: HttpUrl


class SummaryResponse(BaseModel):

    task_id: str

    status: str

    title: str | None = None

    summary: str | None = None

    key_points: list[str] = Field(
        default_factory=list,
    )