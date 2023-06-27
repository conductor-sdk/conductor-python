from .task import TaskInterface
from .task_type import TaskType
from typing_extensions import Self


class InlineTask(TaskInterface):
    def __init__(self, task_ref_name: str, script: str) -> Self:
        super().__init__(
            task_reference_name=task_ref_name,
            task_type=TaskType.INLINE,
            input_parameters={
                "evaluatorType": "javascript",
                "expression":    script,
            }
        )
