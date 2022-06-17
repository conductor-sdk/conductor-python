from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing_extensions import Self


class HumanTask(TaskInterface):
    def __init__(self, task_ref_name: str) -> Self:
        super().__init__(task_ref_name, TaskType.HUMAN)
