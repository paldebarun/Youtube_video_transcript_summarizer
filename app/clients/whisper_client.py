from config import WHISPER_SERVICE_URL

from models.job_model import WhisperJob

from .external_service_base_client import BaseClient


class WhisperClient(BaseClient):

    def __init__(self):

        self.endpoint = (
            f"{WHISPER_SERVICE_URL}/jobs"
        )

    def submit(
        self,
        job: WhisperJob,
    ):

        return self.post(
            self.endpoint,
            job.model_dump(),
        )