from __future__ import annotations
from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.workflow.task.workflow_status import WorkflowStatus


class TerminateTask(TaskInterface):
    def __init__(self, task_ref_name: str, status: WorkflowStatus, termination_reason: str) -> TerminateTask:
        super().__init__(task_ref_name, TaskType.TERMINATE)
        self._input_parameters = {
            "terminationStatus": status,
            "terminationReason": termination_reason
        }
