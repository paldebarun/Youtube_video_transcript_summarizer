import sys
from app.workers.master_worker import MasterWorker
from app.workers.event_worker import EventWorker
from app.workers.summary_worker import SummaryWorker


from app.utils.logger import Logger

logger = Logger.get_logger()


WORKERS = {
    "master": MasterWorker,
    "event": EventWorker,
    "summary": SummaryWorker,
}

def main():

    if len(sys.argv) != 2:
        raise ValueError("Worker name required.")

    worker_name = sys.argv[1]

    worker_class = WORKERS.get(worker_name)

    if worker_class is None:
        raise ValueError(
        f"Unknown worker '{worker_name}'. "
        f"Available workers: {', '.join(WORKERS.keys())}"
    )

    logger.info(f"Starting {worker_name} worker.")

    worker = worker_class()

    worker.start()


if __name__ == "__main__":
    main()