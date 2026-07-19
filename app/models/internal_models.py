from typing import Any

from pydantic import BaseModel


class VideoUnderstandingResult(BaseModel):

    transcript: str

    metadata: dict[str, Any]

    scenes: list[dict[str, Any]]

    ocr: dict[str, Any]

    vision: dict[str, Any]