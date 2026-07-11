from messaging.redis_queue import RedisQueue
from workflow.workflow_orchestrator import WorkflowOrchestrator
from utils.logger import Logger
from config import MASTER_QUEUE

logger=Logger.get_logger()

class MasterWorker:

    def __init__(self):

        self.queue = RedisQueue()
        self.workflow = WorkflowOrchestrator()

    def start(self):

        print("Master Worker Started...")

        while True:

            message = self.queue.pop(MASTER_QUEUE)

            if message is None:
                continue

            task_id = message["task_id"]

            logger.info(f"Received Task: {task_id}")

            self.workflow.handle_task_created(task_id)