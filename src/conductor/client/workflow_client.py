from abc import ABC, abstractmethod
from typing import Optional, List
from conductor.client.http.models.workflow import Workflow
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.http.models.rerun_workflow_request import RerunWorkflowRequest
from conductor.client.http.models.workflow_test_request import WorkflowTestRequest

class WorkflowClient(ABC):
    @abstractmethod
    def startWorkflow(self, startWorkflowRequest: StartWorkflowRequest) -> str:
        pass

    @abstractmethod
    def getWorkflow(self, workflowId: str, includeTasks: Optional[bool] = True) -> Workflow:
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
    
    @abstractmethod
    def testWorkflow(self, testRequest: WorkflowTestRequest) -> Workflow:
        pass



