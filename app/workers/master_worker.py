import redis

from app.messaging.redis_queue import RedisQueue
from app.workflow.workflow_orchestrator import WorkflowOrchestrator
from app.utils.logger import Logger
from app.config import MASTER_QUEUE

logger = Logger.get_logger()


class MasterWorker:

    def __init__(self):
        self.queue = RedisQueue()
        self.workflow = WorkflowOrchestrator()

    def start(self):

        logger.info("Master Worker started.")

        while True:

            try:
                message = self.queue.pop(MASTER_QUEUE)
            except redis.exceptions.TimeoutError:
                continue

            if message is None:
                continue

            try:
                logger.info(f"Message type: {type(message)}")
                logger.info(f"Received message: {message}")

                task_id = message["task_id"]

                logger.info(f"Processing Task: {task_id}")

                self.workflow.handle_task_created(task_id)

                logger.info(f"Completed Task: {task_id}")

            except Exception as e:
                logger.exception(f"Master worker failed: {e}")