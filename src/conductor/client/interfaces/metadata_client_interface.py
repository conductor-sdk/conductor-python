from abc import ABC, abstractmethod
from typing import Optional, List
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.task_def import TaskDef

class MetadataClientInterface(ABC):
    @abstractmethod
    def registerWorkflowDef(self, workflowDef: WorkflowDef, overwrite: Optional[bool]):
        pass

    @abstractmethod
    def updateWorkflowDef(self, workflowDef: WorkflowDef, overwrite: Optional[bool]):
        pass

    @abstractmethod
    def unregisterWorkflowDef(self, workflowName: str, version: int):
        pass

    @abstractmethod
    def getWorkflowDef(self, name: str, version: Optional[int]) -> (Optional[WorkflowDef], str):
        pass

    @abstractmethod
    def getAllWorkflowDefs(self) -> List[WorkflowDef]:
        pass

    @abstractmethod
    def registerTaskDef(self, taskDef: TaskDef):
        pass

    @abstractmethod
    def updateTaskDef(self, taskDef: TaskDef):
        pass

    @abstractmethod
    def unregisterTaskDef(self, taskType: str):
        pass

    @abstractmethod
    def getTaskDef(self, taskType: str) -> TaskDef:
        pass

    @abstractmethod
    def getAllTaskDefs(self) -> List[TaskDef]:
        pass
