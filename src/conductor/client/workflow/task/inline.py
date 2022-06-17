from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing_extensions import Self


class InlineTask(TaskInterface):
    def __init__(self, task_ref_name: str, script: str) -> Self:
        super().__init__(task_ref_name, TaskType.INLINE)
        self._input_parameters = {
            "evaluatorType": "javascript",
            "expression":    script,
        }
