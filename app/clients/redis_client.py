import redis

from config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_DB,
)


class RedisClient:

    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                db=REDIS_DB,
                decode_responses=True,
            )

        return cls._client