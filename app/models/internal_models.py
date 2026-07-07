

from pydantic import BaseModel

class VideoUnderstandingResult(BaseModel):

    transcript: str

    metadata: dict

    scenes: list[dict]

    ocr: dict
    vision: dict