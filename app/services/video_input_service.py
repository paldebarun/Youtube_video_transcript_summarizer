from pathlib import Path
import uuid

from yt_dlp import YoutubeDL

from app.config import DOWNLOAD_DIR
from app.exceptions import VideoDownloadException
from app.utils.logger import Logger

logger = Logger.get_logger()


class VideoInputService:

    def __init__(self):

        self.download_dir = DOWNLOAD_DIR

        self.download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def resolve_video(
        self,
        source: str,
        value: str,
    ) -> Path:

        if source == "local":

            video_path = Path(value)

            if not video_path.exists():

                raise VideoDownloadException(
                    f"Video file does not exist: {video_path}"
                )

            logger.info(
                f"Using local video: {video_path}"
            )

            return video_path

        if source != "youtube":

            raise VideoDownloadException(
                f"Unsupported video source: {source}"
            )

        file_name = str(uuid.uuid4())

        output_template = str(
            self.download_dir / f"{file_name}.%(ext)s"
        )

        options = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": output_template,
            "quiet": True,
            "noplaylist": True,
        }

        try:

            logger.info(
                f"Downloading YouTube video: {value}"
            )

            with YoutubeDL(options) as ydl:

                ydl.download([value])

            video_path = self.download_dir / f"{file_name}.mp4"

            if not video_path.exists():

                raise VideoDownloadException(
                    "Downloaded video was not found."
                )

            logger.info(
                f"Downloaded video: {video_path}"
            )

            return video_path

        except Exception as e:

            raise VideoDownloadException(
                "Failed to resolve video."
            ) from e

    def delete_video(
        self,
        video_path: Path,
    ):

        if video_path.exists():

            video_path.unlink()