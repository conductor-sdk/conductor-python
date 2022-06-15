from __future__ import annotations
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.workflow.task.task import TaskInterface


class SimpleTask(TaskInterface):
    def __init__(self, task_def_name: str, task_reference_name: str) -> SimpleTask:
        super().__init__(task_reference_name, TaskType.SIMPLE)
        self._name = task_def_name
