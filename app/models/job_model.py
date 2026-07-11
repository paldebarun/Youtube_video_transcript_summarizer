from pydantic import BaseModel


class VideoJob(BaseModel):

    task_id: str

    video_path: str