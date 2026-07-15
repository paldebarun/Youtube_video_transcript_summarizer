from pydantic import BaseModel


class VideoJob(BaseModel):

    task_id: str

    video_path: str


class OCRJob(BaseModel):

    task_id: str

    frames: list[str]


class VisionJob(BaseModel):

    task_id: str

    frames: list[str]


class WhisperJob(BaseModel):

    task_id: str

    audio_path: str


class SummaryJob(BaseModel):

    task_id: str