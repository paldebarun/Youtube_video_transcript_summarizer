from app.config import VISION_SERVICE_URL

from app.models.job_model import VisionJob

from app.clients.external_service_base_client import BaseClient


class VisionClient(BaseClient):

    def __init__(self):

        self.endpoint = (
            f"{VISION_SERVICE_URL}/jobs"
        )

    def submit(
        self,
        job: VisionJob,
    ):

        return self.post(
            self.endpoint,
            job.model_dump(),
        )