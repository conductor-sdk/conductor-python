from typing import Optional, List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.workflow import Workflow
from conductor.client.http.models.workflow_run import WorkflowRun
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.http.models.rerun_workflow_request import RerunWorkflowRequest
from conductor.client.workflow_client import WorkflowClient
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.helpers.api_exception_handler import api_exception_handler, for_all_methods

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

    def startWorkflow(self, startWorkflowRequest: StartWorkflowRequest) -> str:
        return self.workflowResourceApi.start_workflow(startWorkflowRequest)

    def executeWorkflow(
        self,
        startWorkflowRequest: StartWorkflowRequest,
        requestId: str,
        name: str,
        version: int,
        waitUntilTaskRef: Optional[str] = None
    ) -> WorkflowRun:
        kwargs = { "wait_until_task_ref" : waitUntilTaskRef } if waitUntilTaskRef else {}
        return self.workflowResourceApi.execute_workflow(startWorkflowRequest, requestId, name, version, **kwargs)

    def pauseWorkflow(self, workflowId: str):
        self.workflowResourceApi.pause_workflow1(workflowId)

    def resumeWorkflow(self, workflowId: str):
        self.workflowResourceApi.resume_workflow1(workflowId)

    def restartWorkflow(self, workflowId: str, useLatestDef: Optional[bool] = False):
        self.workflowResourceApi.restart1(workflowId, use_latest_definitions=useLatestDef)

    def rerunWorkflow(self, workflowId: str, rerunWorkflowRequest: RerunWorkflowRequest):
        self.workflowResourceApi.rerun(rerunWorkflowRequest, workflowId)

    def retryWorkflow(self, workflowId: str, resumeSubworkflowTasks: Optional[bool] = False):
        self.workflowResourceApi.retry1(workflowId, resume_subworkflow_tasks=resumeSubworkflowTasks)

    def terminateWorkflow(self, workflowId: str, reason: Optional[str] = None):
        kwargs = { "reason" : reason } if reason else {}
        self.workflowResourceApi.terminate1(workflowId, **kwargs)

    def getWorkflow(self, workflowId: str, includeTasks: Optional[bool] = True) -> Workflow:
        return self.workflowResourceApi.get_execution_status(workflowId, include_tasks=includeTasks)

    def deleteWorkflow(self, workflowId: str, archiveWorkflow: Optional[bool] = True):
        self.workflowResourceApi.delete(workflowId, archive_workflow=archiveWorkflow)

    def skipTaskFromWorkflow(self, workflowId: str, taskReferenceName: str):
        self.workflowResourceApi.skip_task_from_workflow(workflowId, taskReferenceName)
