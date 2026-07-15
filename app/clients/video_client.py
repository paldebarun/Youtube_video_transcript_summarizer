from config import VIDEO_PROCESSING_SERVICE_URL

from models.job_model import VideoJob

from .external_service_base_client import BaseClient


class VideoClient(BaseClient):

    def __init__(self):

        self.endpoint = (
            f"{VIDEO_PROCESSING_SERVICE_URL}/jobs"
        )

    def submit(
        self,
        job: VideoJob,
    ):

        return self.post(
            self.endpoint,
            job.model_dump(),
        )