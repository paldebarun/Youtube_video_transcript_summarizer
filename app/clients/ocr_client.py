from config import OCR_SERVICE_URL

from models.job_model import OCRJob

from .external_service_base_client import BaseClient


class OCRClient(BaseClient):

    def __init__(self):

        self.endpoint = (
            f"{OCR_SERVICE_URL}/jobs"
        )

    def submit(
        self,
        job: OCRJob,
    ):

        return self.post(
            self.endpoint,
            job.model_dump(),
        )