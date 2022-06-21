from typing_extensions import Self
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.workflow.task.task import TaskInterface


class SimpleTask(TaskInterface):
    # TODO add properties for constructor params
    def __init__(self, task_def_name: str, task_reference_name: str) -> Self:
        super().__init__(
            task_reference_name=task_reference_name,
            task_type=TaskType.SIMPLE,
            task_name=task_def_name,
        )
