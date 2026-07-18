import os
import sys
import time
import textwrap
import subprocess

from pathlib import Path

from app.utils.logger import Logger

logger = Logger.get_logger()


class SupervisorManager:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parent.parent

        self.config_path = Path("/tmp/supervisord.conf")

        self.pid_file = Path("/tmp/supervisord.pid")

        self.socket_file = Path("/tmp/supervisor.sock")

        self.log_file = Path("/tmp/supervisord.log")

        self.process = None

        self.workers = [
            ("master_worker", "master"),
            ("event_worker", "event"),
            ("summary_worker", "summary"),
        ]

    def generate_config(self):

        python_executable = sys.executable

        worker_module = "app.workers.run_worker"

        config = textwrap.dedent(f"""\
[unix_http_server]
file={self.socket_file}

[supervisord]
nodaemon=true
logfile={self.log_file}
pidfile={self.pid_file}

[rpcinterface:supervisor]
supervisor.rpcinterface_factory=supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix://{self.socket_file}

""")

        for program_name, worker_name in self.workers:

            config += textwrap.dedent(f"""\
[program:{program_name}]
command={python_executable} -m {worker_module} {worker_name}
directory={self.project_root.parent}
autostart=true
autorestart=true
startsecs=5
stdout_logfile=/dev/stdout
stderr_logfile=/dev/stderr
stdout_logfile_maxbytes=0
stderr_logfile_maxbytes=0

""")

        self.config_path.write_text(config)

        logger.info(
            f"Generated Supervisor configuration at {self.config_path}"
        )

    def start(self):

        if self.is_running():

            logger.info(
                "Supervisor is already running."
            )

            return

        logger.info(
            "Starting Supervisor..."
        )

        self.process = subprocess.Popen(
            [
                "supervisord",
                "-c",
                str(self.config_path),
            ]
        )

        for _ in range(10):

            if self.is_running():

                logger.info(
                    "Supervisor started successfully."
                )

                return

            time.sleep(1)

        raise RuntimeError(
            "Failed to start Supervisor."
        )

    def stop(self):

        if not self.is_running():

            logger.info(
                "Supervisor is not running."
            )

            return

        logger.info(
            "Stopping Supervisor..."
        )

        subprocess.run(
            [
                "supervisorctl",
                "-c",
                str(self.config_path),
                "shutdown",
            ],
            check=False,
        )

        if self.process:

            try:

                self.process.wait(timeout=10)

            except subprocess.TimeoutExpired:

                logger.warning(
                    "Supervisor did not stop gracefully."
                )

        self.cleanup()

        logger.info(
            "Supervisor stopped."
        )

    def is_running(self) -> bool:

        if not self.pid_file.exists():

            return False

        try:

            pid = int(
                self.pid_file.read_text().strip()
            )

        except Exception:

            return False

        if self._is_process_running(pid):

            return True

        logger.warning(
            "Found stale Supervisor PID. Cleaning up..."
        )

        self.cleanup()

        return False

    @staticmethod
    def _is_process_running(
        pid: int,
    ) -> bool:

        try:

            os.kill(pid, 0)

            return True

        except OSError:

            return False

    def cleanup(self):

        for file in (
            self.pid_file,
            self.socket_file,
            self.log_file,
        ):

            try:

                if file.exists():

                    file.unlink()

            except Exception as e:

                logger.warning(
                    f"Failed to remove {file}: {e}"
                )