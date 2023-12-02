from typing import Optional, List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.workflow import Workflow
from conductor.client.http.models.workflow_run import WorkflowRun
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.http.models.rerun_workflow_request import RerunWorkflowRequest
from conductor.client.http.models.workflow_test_request import WorkflowTestRequest
from conductor.client.workflow_client import WorkflowClient
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.exceptions.api_exception_handler import api_exception_handler, for_all_methods

@for_all_methods(api_exception_handler, ["__init__"])
class OrkesWorkflowClient(OrkesBaseClient, WorkflowClient):
    def __init__(
        self,
        configuration: Configuration
        ):
        super(OrkesWorkflowClient, self).__init__(configuration)

    def startWorkflowByName(
        self,
        name: str,
        input: dict[str, object],
        version: Optional[int] = None,
        correlationId: Optional[str] = None,
        priority: Optional[int] = None,
    ) -> str:
        kwargs = {}
        if version:
            kwargs.update({"version": version})
        if correlationId:
            kwargs.update({"correlation_id": correlationId})
        if priority:
            kwargs.update({"priority": priority})

        return self.workflowResourceApi.start_workflow1(input, name, **kwargs)

    def start_workflow(self, start_workflow_request: StartWorkflowRequest) -> str:
        return self.workflowResourceApi.start_workflow(start_workflow_request)

    def execute_workflow(
        self,
        startWorkflowRequest: StartWorkflowRequest,
        requestId: str,
        name: str,
        version: int,
        waitUntilTaskRef: Optional[str] = None
    ) -> WorkflowRun:
        kwargs = { "wait_until_task_ref" : waitUntilTaskRef } if waitUntilTaskRef else {}
        return self.workflowResourceApi.execute_workflow(startWorkflowRequest, requestId, name, version, **kwargs)

    def pause_workflow(self, workflow_id: str):
        self.workflowResourceApi.pause_workflow1(workflow_id)

    def resume_workflow(self, workflow_id: str):
        self.workflowResourceApi.resume_workflow1(workflow_id)

    def restart_workflow(self, workflow_id: str, use_latest_def: Optional[bool] = False):
        self.workflowResourceApi.restart1(workflow_id, use_latest_definitions=use_latest_def)

    def rerun_workflow(self, workflow_id: str, rerun_workflow_request: RerunWorkflowRequest):
        self.workflowResourceApi.rerun(rerun_workflow_request, workflow_id)

    def retry_workflow(self, workflowId: str, resumeSubworkflowTasks: Optional[bool] = False):
        self.workflowResourceApi.retry1(workflowId, resume_subworkflow_tasks=resumeSubworkflowTasks)

    def terminate_workflow(self, workflow_id: str, reason: Optional[str] = None):
        kwargs = { "reason" : reason } if reason else {}
        self.workflowResourceApi.terminate1(workflow_id, **kwargs)

    def get_workflow(self, workflow_id: str, include_tasks: Optional[bool] = True) -> Workflow:
        return self.workflowResourceApi.get_execution_status(workflow_id, include_tasks=include_tasks)

    def delete_workflow(self, workflow_id: str, archive_workflow: Optional[bool] = True):
        self.workflowResourceApi.delete(workflow_id, archive_workflow=archive_workflow)

    def skip_task_from_workflow(self, workflow_id: str, task_reference_name: str):
        self.workflowResourceApi.skip_task_from_workflow(workflow_id, task_reference_name)

    def test_workflow(self, test_request: WorkflowTestRequest) -> Workflow:
        return self.workflowResourceApi.test_workflow(test_request)