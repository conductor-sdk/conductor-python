from abc import ABC, abstractmethod
from typing import Optional, List
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.task_def import TaskDef


class MetadataClient(ABC):
    @abstractmethod
    def register_workflow_def(
            self,
            workflow_def: WorkflowDef,
            overwrite: Optional[bool]):
        pass

    @abstractmethod
    def update_workflow_def(
            self,
            workflow_def: WorkflowDef,
            overwrite: Optional[bool]):
        pass

    @abstractmethod
    def unregister_workflow_def(self, workflow_name: str, version: int):
        pass

    @abstractmethod
    def get_workflow_def(self, name: str, version: Optional[int]) -> WorkflowDef:
        pass

    @abstractmethod
    def get_all_workflow_defs(self) -> List[WorkflowDef]:
        pass

    @abstractmethod
    def register_task_def(self, task_def: TaskDef):
        pass

    @abstractmethod
    def update_task_def(self, task_def: TaskDef):
        pass

    @abstractmethod
    def unregister_task_def(self, task_type: str):
        pass

    @abstractmethod
    def get_task_def(self, task_type: str) -> TaskDef:
        pass

    @abstractmethod
    def get_all_task_defs(self) -> List[TaskDef]:
        pass
