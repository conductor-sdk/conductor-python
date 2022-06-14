from __future__ import annotations
from conductor.client.workflow.task.task_type import TaskType
from src.conductor.client.workflow.task.workflow_status import WorkflowStatus
from task import TaskInterface


class TerminateTask(TaskInterface):
    def __init__(self, task_ref_name: str, status: WorkflowStatus, termination_reason: str) -> TerminateTask:
        super().__init__(task_ref_name, TaskType.TERMINATE)
        self._input = {
            "terminationStatus": status,
            "terminationReason": termination_reason
        }
