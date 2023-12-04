from typing_extensions import Self

from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType


class HumanTask(TaskInterface):
    def __init__(self, task_ref_name: str) -> Self:
        super().__init__(task_reference_name=task_ref_name, task_type=TaskType.HUMAN)
