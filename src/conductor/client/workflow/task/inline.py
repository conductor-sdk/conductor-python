from __future__ import annotations
from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType


class InlineTask(TaskInterface):
    def __init__(self, task_ref_name: str, script: str) -> InlineTask:
        super().__init__(task_ref_name, TaskType.INLINE)
        self._input_parameters = {
            "evaluatorType": "javascript",
            "expression":    script,
        }
