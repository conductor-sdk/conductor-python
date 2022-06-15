from __future__ import annotations
from conductor.client.workflow.task.task_type import TaskType
from task import TaskInterface


class WaitTask(TaskInterface):
    def __init__(self, task_ref_name: str) -> WaitTask:
        super().__init__(task_ref_name, TaskType.WAIT)


class WaitForDurationTask(WaitTask):
    def __init__(self, task_ref_name: str, duration_time_seconds: int) -> WaitForDurationTask:
        super().__init__(task_ref_name)
        self._input_parameters = {
            "duration": str(duration_time_seconds)
        }


class WaitUntilTask(WaitTask):
    def __init__(self, task_ref_name: str, date_time: str) -> WaitForDurationTask:
        super().__init__(task_ref_name)
        self._input_parameters = {
            "until": date_time
        }
