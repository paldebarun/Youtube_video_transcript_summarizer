import httpx

from config import VIDEO_PROCESSING_SERVICE_URL
from models.job_model import VideoJob


class VideoProcessingService:

    def __init__(self):

        self.endpoint = (
            f"{VIDEO_PROCESSING_SERVICE_URL}/jobs"
        )

    def submit(
        self,
        job: VideoJob,
    ):

        response = httpx.post(
            self.endpoint,
            json=job.model_dump(),
            timeout=30,
        )

        response.raise_for_status()

        return None