from __future__ import annotations
from conductor.client.workflow.task.http_input import HttpInput
from conductor.client.workflow.task.task_type import TaskType
from task import TaskInterface


class HttpTask(TaskInterface):
    def __init__(self, task_ref_name: str, http_input: HttpInput) -> HttpTask:
        super().__init__(task_ref_name, TaskType.HTTP)
        self._input_parameters = {
            "http_request": http_input
        }
