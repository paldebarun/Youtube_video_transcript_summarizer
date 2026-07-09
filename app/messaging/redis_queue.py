import json
from clients.redis_client import RedisClient


class RedisQueue:

    def __init__(self):

        self.client = RedisClient.get_client()

    def push(
        self,
        queue_name: str,
        message: dict,
    ):

        self.client.rpush(
            queue_name,
            json.dumps(message),
        )

    def pop(
        self,
        queue_name: str,
        timeout: int = 0,
    ):

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