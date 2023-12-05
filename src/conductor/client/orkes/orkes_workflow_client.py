"""Orkes Workflow Client

The class in this module allows management of workflow executions.
"""

from typing import Optional

from conductor.client.exceptions.api_exception_handler import (
    api_exception_handler, for_all_methods)
from conductor.client.http.models import SkipTaskRequest
from conductor.client.http.models.rerun_workflow_request import \
    RerunWorkflowRequest
from conductor.client.http.models.start_workflow_request import \
    StartWorkflowRequest
from conductor.client.http.models.workflow import Workflow
from conductor.client.http.models.workflow_run import WorkflowRun
from conductor.client.http.models.workflow_test_request import \
    WorkflowTestRequest
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.workflow_client import WorkflowClient


@for_all_methods(api_exception_handler, ["__init__"])
class OrkesWorkflowClient(OrkesBaseClient, WorkflowClient):
    """
    A class to manage workflow executions by allowing executing workflows both
    synchronously and asynchronously and sending signals to the workflow.
    """

    def start_workflow_by_name(
        self,
        name: str,
        input: dict[str, object],
        version: Optional[int] = None,
        correlation_id: Optional[str] = None,
        priority: Optional[int] = None,
    ) -> str:
        kwargs = {}
        if version:
            kwargs.update({"version": version})
        if correlation_id:
            kwargs.update({"correlation_id": correlation_id})
        if priority:
            kwargs.update({"priority": priority})

        return self.workflow_resource_api.start_workflow1(input, name, **kwargs)

    def start_workflow(self, start_workflow_request: StartWorkflowRequest) -> str:
        return self.workflow_resource_api.start_workflow(start_workflow_request)

    def execute_workflow(
        self,
        start_workflow_request: StartWorkflowRequest,
        request_id: str,
        name: str,
        version: int,
        wait_until_task_ref: Optional[str] = None,
    ) -> WorkflowRun:
        kwargs = (
            {"wait_until_task_ref": wait_until_task_ref} if wait_until_task_ref else {}
        )
        return self.workflow_resource_api.execute_workflow(
            start_workflow_request, request_id, name, version, **kwargs
        )

    def pause_workflow(self, workflow_id: str):
        self.workflow_resource_api.pause_workflow(workflow_id)

    def resume_workflow(self, workflow_id: str):
        self.workflow_resource_api.resume_workflow(workflow_id)

    def restart_workflow(
        self, workflow_id: str, use_latest_def: Optional[bool] = False
    ):
        self.workflow_resource_api.restart(
            workflow_id, use_latest_definitions=use_latest_def
        )

    def rerun_workflow(
        self, workflow_id: str, rerun_workflow_request: RerunWorkflowRequest
    ):
        self.workflow_resource_api.rerun(rerun_workflow_request, workflow_id)

    def retry_workflow(
        self, workflow_id: str, resume_subworkflow_tasks: Optional[bool] = False
    ):
        self.workflow_resource_api.retry(
            workflow_id, resume_subworkflow_tasks=resume_subworkflow_tasks
        )

    def terminate_workflow(self, workflow_id: str, reason: Optional[str] = None):
        kwargs = {"reason": reason} if reason else {}
        self.workflow_resource_api.terminate1(workflow_id, **kwargs)

    def get_workflow(
        self, workflow_id: str, include_tasks: Optional[bool] = True
    ) -> Workflow:
        return self.workflow_resource_api.get_execution_status(
            workflow_id, include_tasks=include_tasks
        )

    def delete_workflow(
        self, workflow_id: str, archive_workflow: Optional[bool] = True
    ):
        self.workflow_resource_api.delete(workflow_id, archive_workflow=archive_workflow)

    def skip_task_from_workflow(
        self, workflow_id: str, task_reference_name: str, request: SkipTaskRequest
    ):
        self.workflow_resource_api.skip_task_from_workflow(
            workflow_id, task_reference_name, request
        )

    def test_workflow(self, test_request: WorkflowTestRequest) -> Workflow:
        return self.workflow_resource_api.test_workflow(test_request)
