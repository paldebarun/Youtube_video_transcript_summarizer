from messaging.redis_queue import RedisQueue

from config import SUMMARY_QUEUE

from models.internal_models import VideoUnderstandingResult
from models.task_document import ServiceType
from services.task_service import TaskService
from services.summarization_service import SummarizationService

from utils.logger import Logger

logger = Logger.get_logger()


class SummaryWorker:

    def __init__(self):

        self.queue = RedisQueue()

        self.task_service = TaskService()

        self.summarization_service = SummarizationService()

    def start(self):

        logger.info(
            "Summary Worker Started."
        )

        while True:

            message = self.queue.pop(
                SUMMARY_QUEUE,
            )

            if message is None:

                continue

            try:

                task_id = message["task_id"]

                logger.info(
                    f"Generating summary for task: {task_id}"
                )

                task = self.task_service.get_task(
                    task_id,
                )

                video = VideoUnderstandingResult(
                    transcript=task.whisper.result["text"],
                    metadata=task.video_processing.result["metadata"],
                    scenes=task.video_processing.result["scenes"],
                    ocr=task.ocr.result,
                    vision=task.vision.result,
                )

                summary = self.summarization_service.summarize(
                    video,
                )

                self.task_service.update_summary(
                    task_id,
                    summary.model_dump(),
                )

                logger.info(
                    f"Summary completed for task: {task_id}"
                )

            except Exception as e:

                logger.error(
                    f"Summary generation failed: {e}"
                )

                self.task_service.mark_service_failed(
                    task_id,
                    service=ServiceType.SUMMARY,
                    error=str(e),
                )