import json
from app.clients.redis_client import RedisClient
from app.utils.logger import Logger

logger=Logger.get_logger()

class RedisQueue:

    def __init__(self):

        self.client = RedisClient.get_client()

    def push(
        self,
        queue_name: str,
        message: dict,
    ):
        logger.info(f"Pushing to '{queue_name}' queue with message: {message}")

        try:
            result = self.client.rpush(
                queue_name,
                json.dumps(message),
            )

            logger.info(
                f"RPUSH returned {result} for queue '{queue_name}'"
            )

        except Exception as e:
            logger.exception(f"Redis push failed: {e}")
            raise

    def pop(
        self,
        queue_name: str,
        timeout: int = 30,          
    ):
        logger.info(f"Poping from :{queue_name}")
        result = self.client.blpop(
            queue_name,
            timeout=timeout,
        )

        if result is None:
            return None

        _, message = result

        return json.loads(message)

    def length(
        self,
        queue_name: str,
    ):

        return self.client.llen(queue_name)