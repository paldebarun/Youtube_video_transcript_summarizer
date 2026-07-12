import httpx

from config import (
    COUCHDB_HOST,
    COUCHDB_PORT,
    COUCHDB_USERNAME,
    COUCHDB_PASSWORD,
    COUCHDB_DATABASE,
)

from utils.logger import Logger

logger = Logger.get_logger()


class CouchDBClient:

    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = httpx.Client(
                base_url=f"http://{COUCHDB_HOST}:{COUCHDB_PORT}",
                auth=(
                    COUCHDB_USERNAME,
                    COUCHDB_PASSWORD,
                ),
                timeout=60,
            )

            cls._initialize_database()

        return cls._client

    @classmethod
    def _initialize_database(cls):

        try:

            # Check CouchDB server
            response = cls._client.get("/")

            response.raise_for_status()

            logger.info("Successfully connected to CouchDB.")

            # Check if database exists
            response = cls._client.get(
                f"/{COUCHDB_DATABASE}"
            )

            if response.status_code == 404:

                logger.info(
                    f"Database '{COUCHDB_DATABASE}' does not exist. Creating..."
                )

                response = cls._client.put(
                    f"/{COUCHDB_DATABASE}"
                )

                response.raise_for_status()

                logger.info(
                    f"Database '{COUCHDB_DATABASE}' created successfully."
                )

            elif response.status_code == 200:

                logger.info(
                    f"Database '{COUCHDB_DATABASE}' already exists."
                )

            else:

                response.raise_for_status()

        except Exception:

            logger.exception(
                "Failed to initialize CouchDB."
            )

            raise