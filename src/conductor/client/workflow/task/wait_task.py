from typing_extensions import Self
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.workflow.task.task import TaskInterface


class WaitTask(TaskInterface):
    def __init__(self, task_ref_name: str) -> Self:
        super().__init__(task_ref_name, TaskType.WAIT)


class WaitForDurationTask(WaitTask):
    def __init__(self, task_ref_name: str, duration_time_seconds: int) -> Self:
        super().__init__(task_ref_name)
        self._input_parameters = {
            "duration": str(duration_time_seconds)
        }


class WaitUntilTask(WaitTask):
    def __init__(self, task_ref_name: str, date_time: str) -> Self:
        super().__init__(task_ref_name)
        self._input_parameters = {
            "until": date_time
        }
