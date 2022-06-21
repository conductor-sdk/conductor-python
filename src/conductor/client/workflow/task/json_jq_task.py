from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing_extensions import Self


class JsonJQTask(TaskInterface):
    # TODO add properties for constructor params
    def __init__(self, task_ref_name: str, script: str) -> Self:
        super().__init__(
            task_reference_name=task_ref_name,
            task_type=TaskType.JSON_JQ_TRANSFORM,
            input_parameters={
                "queryExpression": script
            }
        )
