from .task import TaskInterface
from .task_type import TaskType
from typing_extensions import Self


class HumanTask(TaskInterface):
    def __init__(self, task_ref_name: str) -> Self:
        super().__init__(
            task_reference_name=task_ref_name,
            task_type=TaskType.HUMAN
        )
