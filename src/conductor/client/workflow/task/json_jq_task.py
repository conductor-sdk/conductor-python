from __future__ import annotations
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.workflow.task.task import TaskInterface


class JsonJQTask(TaskInterface):
    def __init__(self, task_ref_name: str, script: str) -> JsonJQTask:
        super().__init__(task_ref_name, TaskType.JSON_JQ_TRANSFORM)
        self._input_parameters = {
            "queryExpression": script
        }
