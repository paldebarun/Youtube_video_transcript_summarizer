from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def resolve_path(env_name: str, default: str) -> Path:
    """
    Resolve a directory path from an environment variable.

    Relative paths are resolved relative to BASE_DIR.
    Absolute paths are used directly.
    """

    path = Path(os.getenv(env_name, default))

    if not path.is_absolute():
        path = BASE_DIR / path

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

WHISPER_SERVICE_URL = os.getenv(
    "WHISPER_SERVICE_URL",
    "http://localhost:2000",
)

VIDEO_PROCESSING_SERVICE_URL = os.getenv(
    "VIDEO_PROCESSING_SERVICE_URL",
    "http://localhost:3000",
)

OCR_SERVICE_URL = os.getenv(
    "OCR_SERVICE_URL",
    "http://localhost:4000",
)

DOWNLOAD_DIR = resolve_path(
    "DOWNLOAD_DIR",
    "downloads",
)

VISION_SERVICE_URL = os.getenv(
    "VISION_SERVICE_URL",
    "http://localhost:9000",
)


REDIS_HOST = os.getenv(
    "REDIS_HOST",
    "localhost",
)

REDIS_PORT = int(
    os.getenv(
        "REDIS_PORT",
        6379,
    )
)

REDIS_PASSWORD = os.getenv(
    "REDIS_PASSWORD",
)

MASTER_QUEUE = "youtube_master_queue"

SUMMARY_QUEUE = "youtube_summary_queue"

REDIS_EVENT_STREAM = "youtube_events"

EVENT_CONSUMER_GROUP = "workflow_group"

EVENT_CONSUMER_NAME = "workflow_consumer"

REDIS_DB = int(os.getenv("REDIS_DB", 0))


COUCHDB_HOST = os.getenv("COUCHDB_HOST", "couchdb")

COUCHDB_PORT = int(os.getenv("COUCHDB_PORT", 5984))

COUCHDB_USERNAME = os.getenv("COUCHDB_USERNAME", "admin")

COUCHDB_PASSWORD = os.getenv("COUCHDB_PASSWORD", "password")

COUCHDB_DATABASE = os.getenv(
    "COUCHDB_DATABASE",
    "youtube_tasks",
)