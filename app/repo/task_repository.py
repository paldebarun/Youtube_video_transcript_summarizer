from datetime import UTC, datetime

from clients.couchdb_client import CouchDBClient

from config import COUCHDB_DATABASE

from models.task_document import (
    TaskDocument,
    WorkflowStage,
    ServiceStatus
)


class TaskRepository:

    def __init__(self):

        self.client = CouchDBClient.get_client()

        self.database = COUCHDB_DATABASE

    def create_task(
        self,
        task: TaskDocument,
    ):

        response = self.client.put(
            f"/{self.database}/{task.id}",
            json=task.model_dump(
                by_alias=True,
                mode="json",
            ),
        )

        response.raise_for_status()

        return response.json()

    def get_task(
        self,
        task_id: str,
    ) -> TaskDocument:

        response = self.client.get(
            f"/{self.database}/{task_id}"
        )

        response.raise_for_status()

        return TaskDocument.model_validate(
            response.json()
        )

    def update_task(
        self,
        task: TaskDocument,
    ):

        existing = self.client.get(
            f"/{self.database}/{task.id}"
        ).json()

        task_dict = task.model_dump(
            by_alias=True,
            mode="json",
        )

        task_dict["_rev"] = existing["_rev"]

        response = self.client.put(
            f"/{self.database}/{task.id}",
            json=task_dict,
        )

        response.raise_for_status()

    def update_workflow_stage(
        self,
        task_id: str,
        stage: WorkflowStage,
    ):

        task = self.get_task(task_id)

        task.workflow_stage = stage

        self.update_task(task)

    def update_service_status(
        self,
        task_id: str,
        service_name: str,
        status: ServiceStatus,
    ):

        task = self.get_task(task_id)

        service = getattr(
            task,
            service_name,
        )

        service.status = status

        if status == ServiceStatus.PROCESSING:

            service.started_at = datetime.now(UTC)

        elif status in (
            ServiceStatus.COMPLETED,
            ServiceStatus.FAILED,
        ):

            service.completed_at = datetime.utcnow()

        self.update_task(task)

    def update_service_result(
            self,
            task_id: str,
            service_name: str,
            result,
        ):

            task = self.get_task(task_id)

            service = getattr(
                task,
                service_name,
            )

            service.status = ServiceStatus.COMPLETED

            service.completed_at = datetime.now(UTC)

            service.error = None

            service.result = result

            self.update_task(task)

    def update_summary(
        self,
        task_id: str,
        summary,
    ):

        task = self.get_task(task_id)

        task.summary.status = ServiceStatus.COMPLETED

        task.summary.completed_at = datetime.now(UTC)

        task.summary.result = summary

        task.workflow_stage = WorkflowStage.COMPLETED

        task.status = ServiceStatus.COMPLETED

        task.completed_at = datetime.now(UTC)

        self.update_task(task)

    def mark_failed(
        self,
        task_id: str,
        error: str,
    ):

        task = self.get_task(task_id)

        task.status = ServiceStatus.FAILED

        task.workflow_stage = WorkflowStage.FAILED

        task.completed_at = datetime.utcnow()

        self.update_task(task)

    def delete_task(
        self,
        task_id: str,
    ):

        task = self.client.get(
            f"/{self.database}/{task_id}"
        ).json()

        response = self.client.delete(
            f"/{self.database}/{task_id}",
            params={
                "rev": task["_rev"],
            },
        )

        response.raise_for_status()