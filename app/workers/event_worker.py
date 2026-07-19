import json

from app.models.event_model import WorkflowEvent

from app.messaging.redis_stream import RedisStream

from app.workflow.workflow_orchestrator import WorkflowOrchestrator

from app.config import (
    EVENT_STREAM,
    EVENT_CONSUMER_GROUP,
    EVENT_CONSUMER_NAME,
)

from app.utils.logger import Logger

logger = Logger.get_logger()


class EventWorker:

    def __init__(self):

        self.stream = RedisStream()

        self.workflow = WorkflowOrchestrator()

        self.stream.create_consumer_group(
            EVENT_STREAM,
            EVENT_CONSUMER_GROUP,
        )

    def start(self):

        logger.info(
            "Event Worker Started."
        )

        while True:

            events = self.stream.read(
                EVENT_STREAM,
                EVENT_CONSUMER_GROUP,
                EVENT_CONSUMER_NAME,
            )

            if not events:

                continue

            for _, messages in events:

                for message_id, event_data in messages:

                    try:

                        event_data = dict(event_data)

                        payload = event_data.get("payload")

                        if isinstance(payload, str) and payload:
                            event_data["payload"] = json.loads(payload)

                        error = event_data.get("error")

                        if error == "None":
                            event_data["error"] = None

                        event = WorkflowEvent(
                            **event_data,
                        )

                        self.workflow.handle_event(
                            event,
                        )

                        self.stream.acknowledge(
                            EVENT_STREAM,
                            EVENT_CONSUMER_GROUP,
                            message_id,
                        )

                    except Exception as e:

                        logger.error(
                            f"Failed processing event {message_id}: {e}"
                        )