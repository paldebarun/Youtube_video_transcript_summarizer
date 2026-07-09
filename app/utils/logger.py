import logging
import sys

from colorama import Fore, Style, init

init(autoreset=True)


class ColoredFormatter(logging.Formatter):

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):

        color = self.COLORS.get(
            record.levelno,
            Fore.WHITE,
        )

        log_message = super().format(record)

        return f"{color}{log_message}{Style.RESET_ALL}"


class Logger:

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger is not None:
            return cls._logger

        logger = logging.getLogger("youtube_summarizer")

        logger.setLevel(logging.DEBUG)

        logger.propagate = False

        if not logger.handlers:

            handler = logging.StreamHandler(sys.stdout)

            formatter = ColoredFormatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            handler.setFormatter(formatter)

            logger.addHandler(handler)

        cls._logger = logger

        return logger