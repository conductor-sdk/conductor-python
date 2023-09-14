from abc import ABC, abstractmethod
from typing import Optional, List
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.workflow_tag import WorkflowTag
from conductor.client.http.models.task_def import TaskDef

class MetadataClient(ABC):
    @abstractmethod
    def registerWorkflowDef(self, workflowDef: WorkflowDef, overwrite: Optional[bool]):
        pass

    @abstractmethod
    def unregisterWorkflowDef(self, workflowId: str, version: int):
        pass

    @abstractmethod
    def updateWorkflowDef(self):
        pass

    @abstractmethod
    def getWorkflowDef(self, name: str, version: Optional[int]) -> (Optional[WorkflowDef], str):
        pass

    @abstractmethod
    def getAllWorkflowDefs(self) -> List[WorkflowDef]:
        pass

    @abstractmethod
    def registerTaskDef(self):
        pass

    @abstractmethod
    def unregisterTaskDef(self):
        pass

    @abstractmethod
    def updateTaskDef(self):
        pass

    @abstractmethod
    def getTaskDef(self, taskType: str) -> TaskDef:
        pass

    @abstractmethod
    def getAllTaskDefs(self) -> List[TaskDef]:
        pass

    @abstractmethod
    def getTags(self):
        pass

    @abstractmethod
    def setWorkflowTags(self):
        pass
    
    @abstractmethod
    def deleteWorkflowTags(self):
        pass
    
    @abstractmethod
    def getWorkflowTags(self, workflowName: str) -> List[WorkflowTag]:
        pass
    
    @abstractmethod
    def setWorkflowTags(self):
        pass

    @abstractmethod
    def setTaskTags(self):
        pass
    
    @abstractmethod
    def deleteTaskTags(self):
        pass

    @abstractmethod
    def getTaskTags(self):
        pass

    @abstractmethod
    def setTaskTags(self):
        pass
    
