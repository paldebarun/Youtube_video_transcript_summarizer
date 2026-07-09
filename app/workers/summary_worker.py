from messaging.redis_queue import RedisQueue

from services.summarization_service import SummarizationService

from config import SUMMARY_QUEUE


class SummaryWorker:

    def __init__(self):

        self.queue = RedisQueue()

        self.summarization_service = SummarizationService()

    def start(self):

        print("Summary Worker Started...")

        while True:

            message = self.queue.pop(SUMMARY_QUEUE)

            if message is None:
                continue

            task_id = message["task_id"]

            self.summarization_service.generate(
                task_id,
            )