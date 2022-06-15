from __future__ import annotations
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.workflow.task.task import TaskInterface


class HumanTask(TaskInterface):
    def __init__(self, task_ref_name: str) -> HumanTask:
        super().__init__(task_ref_name, TaskType.HUMAN)
