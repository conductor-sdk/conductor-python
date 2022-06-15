from __future__ import annotations
from conductor.client.workflow.task.task_type import TaskType
from task import TaskInterface


class SetVariableTask(TaskInterface):
    def __init__(self, task_ref_name: str) -> SetVariableTask:
        super().__init__(task_ref_name, TaskType.SET_VARIABLE)
