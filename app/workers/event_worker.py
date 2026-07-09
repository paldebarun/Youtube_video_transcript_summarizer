from messaging.redis_stream import RedisStream
from workflow.workflow_orchestrator import WorkflowOrchestrator

from config import (
    REDIS_EVENT_STREAM,
    EVENT_CONSUMER_GROUP,
    EVENT_CONSUMER_NAME,
)


class EventWorker:

    def __init__(self):

        self.stream = RedisStream()

        self.workflow = WorkflowOrchestrator()

        self.stream.create_consumer_group(
            REDIS_EVENT_STREAM,
            EVENT_CONSUMER_GROUP,
        )

    def start(self):

        print("Event Worker Started...")

        while True:

            events = self.stream.read(
                REDIS_EVENT_STREAM,
                EVENT_CONSUMER_GROUP,
                EVENT_CONSUMER_NAME,
            )

            if not events:
                continue

            for _, messages in events:

                for message_id, event in messages:

                    self.workflow.handle_event(event)

                    self.stream.acknowledge(
                        REDIS_EVENT_STREAM,
                        EVENT_CONSUMER_GROUP,
                        message_id,
                    )