from pydantic import BaseModel


class Frame(BaseModel):

    start: float

    end: float

    frame_path: str


class VideoJob(BaseModel):

    task_id: str

    video_path: str


class OCRJob(BaseModel):

    task_id: str

    frames: list[Frame]


class VisionJob(BaseModel):

    task_id: str

    frames: list[Frame]


class WhisperJob(BaseModel):

    task_id: str

    audio_path: str


class SummaryJob(BaseModel):

    task_id: str