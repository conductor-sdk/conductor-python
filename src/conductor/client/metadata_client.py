from abc import ABC, abstractmethod
from typing import Optional, List
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.task_def import TaskDef
from conductor.client.http.models.tag_object import TagObject
from conductor.client.http.models.tag_string import TagString

class MetadataClient(ABC):
    @abstractmethod
    def registerWorkflowDef(self, workflowDef: WorkflowDef, overwrite: Optional[bool]):
        pass

    @abstractmethod
    def updateWorkflowDef(self, workflowDef: WorkflowDef, overwrite: Optional[bool]):
        pass

    @abstractmethod
    def unregisterWorkflowDef(self, name: str, version: int):
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

    @abstractmethod
    def addWorkflowTag(self, tagObj: TagObject, workflowName: str):
        pass

    @abstractmethod
    def deleteWorkflowTag(self, tagStr: TagString, workflowName: str):
        pass

    @abstractmethod
    def getWorkflowTags(self, workflowName: str) -> List[TagObject]:
        pass

    @abstractmethod
    def setWorkflowTags(self, tagObjs: List[TagObject], workflowName: str):
        pass

    @abstractmethod
    def addTaskTag(self, tagObj: TagObject, taskName: str):
        pass
    
    @abstractmethod
    def deleteTaskTag(self, tagStr: TagString, taskName: str):
        pass

    @abstractmethod
    def getTaskTags(self, taskName: str) -> List[TagObject]:
        pass
        
    @abstractmethod
    def setTaskTags(self, tagObjs: List[TagObject], taskName: str):
        pass
            