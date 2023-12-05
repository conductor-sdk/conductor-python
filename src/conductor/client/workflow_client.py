from abc import ABC, abstractmethod
from typing import List, Optional

from conductor.client.http.models import SkipTaskRequest, WorkflowRun
from conductor.client.http.models.rerun_workflow_request import \
    RerunWorkflowRequest
from conductor.client.http.models.start_workflow_request import \
    StartWorkflowRequest
from conductor.client.http.models.workflow import Workflow
from conductor.client.http.models.workflow_test_request import \
    WorkflowTestRequest


class WorkflowClient(ABC):
    @abstractmethod
    def start_workflow(self, start_workflow_request: StartWorkflowRequest) -> str:
        pass

    @abstractmethod
    def get_workflow(
        self, workflow_id: str, include_tasks: Optional[bool] = True
    ) -> Workflow:
        pass

    @abstractmethod
    def delete_workflow(
        self, workflow_id: str, archive_workflow: Optional[bool] = True
    ):
        pass

    @abstractmethod
    def terminate_workflow(self, workflow_id: str, reason: Optional[str] = None):
        pass

    @abstractmethod
    def execute_workflow(
        self,
        start_workflow_request: StartWorkflowRequest,
        request_id: str,
        name: str,
        version: int,
        wait_until_task_ref: Optional[str] = None,
    ) -> WorkflowRun:
        pass

    @abstractmethod
    def pause_workflow(self, workflow_id: str):
        pass

    @abstractmethod
    def resume_workflow(self, workflow_id: str):
        pass

    @abstractmethod
    def restart_workflow(
        self, workflow_id: str, use_latest_def: Optional[bool] = False
    ):
        pass

    @abstractmethod
    def retry_workflow(
        self, workflow_id: str, resume_subworkflow_tasks: Optional[bool] = False
    ):
        pass

    @abstractmethod
    def rerun_workflow(
        self, workflow_id: str, rerun_workflow_request: RerunWorkflowRequest
    ):
        pass

    @abstractmethod
    def skip_task_from_workflow(
        self, workflow_id: str, task_reference_name: str, request: SkipTaskRequest
    ):
        pass

    @abstractmethod
    def test_workflow(self, test_request: WorkflowTestRequest) -> Workflow:
        pass
