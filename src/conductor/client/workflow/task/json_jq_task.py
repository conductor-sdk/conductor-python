from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing_extensions import Self


class JsonJQTask(TaskInterface):
    def __init__(self, task_ref_name: str, script: str) -> Self:
        super().__init__(task_ref_name, TaskType.JSON_JQ_TRANSFORM)
        self._input_parameters = {
            "queryExpression": script
        }
