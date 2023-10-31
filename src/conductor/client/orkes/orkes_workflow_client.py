from typing import Optional, List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.rest import ApiException
from conductor.client.http.models.workflow import Workflow
from conductor.client.http.models.workflow_run import WorkflowRun
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.http.models.rerun_workflow_request import RerunWorkflowRequest
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi
from conductor.client.workflow_client import WorkflowClient

class OrkesWorkflowClient(WorkflowClient):
    def __init__(self, configuration: Configuration):
        api_client = ApiClient(configuration)
        self.workflowResourceApi = WorkflowResourceApi(api_client)

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

    def getWorkflow(self, workflowId: str, includeTasks: Optional[bool] = True) -> (Optional[Workflow], str):
        workflow = None
        error = None

        try:
            workflow = self.workflowResourceApi.get_execution_status(workflowId, include_tasks=includeTasks)
        except ApiException as e:
            message = e.reason if e.reason else e.body
            error = message

        return workflow, error

    def deleteWorkflow(self, workflowId: str, archiveWorkflow: Optional[bool] = True):
        self.workflowResourceApi.delete(workflowId, archive_workflow=archiveWorkflow)

    def skipTaskFromWorkflow(self, workflowId: str, taskReferenceName: str):
        self.workflowResourceApi.skip_task_from_workflow(workflowId, taskReferenceName)
