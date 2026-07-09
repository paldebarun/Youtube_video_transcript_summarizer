import redis
from clients.redis_client import RedisClient



class RedisStream:

    def __init__(self):

        self.client = RedisClient.get_client()

    def publish(
        self,
        stream_name: str,
        event: dict,
    ):

        return self.client.xadd(
            stream_name,
            event,
        )

    def create_consumer_group(
        self,
        stream_name: str,
        group_name: str,
    ):

        try:

            self.client.xgroup_create(
                stream_name,
                group_name,
                id="0",
                mkstream=True,
            )

        except redis.exceptions.ResponseError as e:

            if "BUSYGROUP" not in str(e):
                raise

    def read(
        self,
        stream_name: str,
        group_name: str,
        consumer_name: str,
        count: int = 1,
        block: int = 5000,
    ):

        return self.client.xreadgroup(
            group_name,
            consumer_name,
            {stream_name: ">"},
            count=count,
            block=block,
        )

    def acknowledge(
        self,
        stream_name: str,
        group_name: str,
        message_id: str,
    ):

        self.client.xack(
            stream_name,
            group_name,
            message_id,
        )