import redis
from app.clients.redis_client import RedisClient
from app.utils.logger import Logger
logger=Logger.get_logger()


class RedisStream:

    def __init__(self):

        self.client = RedisClient.get_client()

    def publish(
        self,
        stream_name: str,
        event: dict,
    ):
        logger.info(f"Publishing event : {event} to {stream_name} stream")
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
            logger.info(f"creating consumer with group name :{group_name} and stream name : {stream_name}")
            self.client.xgroup_create(
                stream_name,
                group_name,
                id="0",
                mkstream=True,
            )
            logger.info(f"create consumer with group name :{group_name} and stream name : {stream_name}")
            
           
        except redis.exceptions.ResponseError as e:
            logger.error(f"exception while creating consumer with group name :{group_name} and stream name : {stream_name} with this error : {e}")
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
        logger.info(f"reading from {stream_name} stream, {group_name} group, and {consumer_name} consumer")
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
        logger.info(f"acknowledging for {stream_name} stream, {group_name} group")
        self.client.xack(
            stream_name,
            group_name,
            message_id,
        )