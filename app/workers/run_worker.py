import sys

from config import WORKERS

from utils.logger import Logger

logger = Logger.get_logger()




def main():

    if len(sys.argv) != 2:
        raise ValueError("Worker name required.")

    worker_name = sys.argv[1]

    worker_class = WORKERS.get(worker_name)

    if worker_class is None:
        raise ValueError(f"Unknown worker '{worker_name}'")

    logger.info(f"Starting {worker_name} worker.")

    worker = worker_class()

    worker.start()


if __name__ == "__main__":
    main()