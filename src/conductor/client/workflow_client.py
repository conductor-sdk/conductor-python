from abc import ABC, abstractmethod
from typing import Optional, List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.rest import ApiException
from conductor.client.http.models.workflow import Workflow
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.http.models.rerun_workflow_request import RerunWorkflowRequest
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi


class WorkflowClient(ABC):
    @abstractmethod
    def startWorkflow(self, startWorkflowRequest: StartWorkflowRequest) -> str:
        pass

    @abstractmethod
    def getWorkflow(self, workflowId: str, includeTasks: Optional[bool] = True) -> (Optional[Workflow], str):
        pass

    @abstractmethod
    def deleteWorkflow(self, workflowId: str, archiveWorkflow: Optional[bool] = True):
        pass

    @abstractmethod
    def terminateWorkflow(self, workflowId: str, reason: Optional[str] = None):
        pass

    @abstractmethod
    def executeWorkflow(self):
        pass

    @abstractmethod
    def pauseWorkflow(self, workflowId: str):
        pass

    @abstractmethod
    def resumeWorkflow(self, workflowId: str):
        pass

    @abstractmethod
    def restartWorkflow(self, workflowId: str, useLatestDef: Optional[bool] = False):
        pass

    @abstractmethod
    def retryWorkflow(self):
        pass

    @abstractmethod
    def rerunWorkflow(self, workflowId: str, rerunWorkflowRequest: RerunWorkflowRequest):
        pass

    @abstractmethod
    def skipTaskFromWorkflow(self, workflowId: str, taskReferenceName: str):
        pass



