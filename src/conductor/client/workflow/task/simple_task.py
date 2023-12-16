from typing import Any

from typing_extensions import Self

from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType


class SimpleTask(TaskInterface):
    def __init__(self, task_def_name: str, task_reference_name: str, execute_fn: TaskInterface = None) -> Self:
        super().__init__(
            task_reference_name=task_reference_name,
            task_type=TaskType.SIMPLE,
            task_name=task_def_name,
            executor=execute_fn
        )

    def __getattribute__(self, __name: str) -> Any:
        try:
            val = super().__getattribute__(__name)
            return val
        except AttributeError as ae:
            if not __name.startswith('_'):
                return '${' + self.task_reference_name + '.output.' + __name + '}'
            raise ae
