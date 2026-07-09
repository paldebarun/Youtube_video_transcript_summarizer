from messaging.redis_queue import RedisQueue
from workflow.workflow_orchestrator import WorkflowOrchestrator

from config import MASTER_QUEUE


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

            print(f"Received Task: {task_id}")

            self.workflow.start(task_id)