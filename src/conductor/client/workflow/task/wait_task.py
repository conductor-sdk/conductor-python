from abc import ABC, abstractmethod
from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing_extensions import Self


class WaitTask(TaskInterface, ABC):
    # TODO add properties for constructor params
    @abstractmethod
    def __init__(self, task_ref_name: str) -> Self:
        super().__init__(
            task_reference_name=task_ref_name,
            task_type=TaskType.WAIT
        )


class WaitForDurationTask(WaitTask):
    # TODO add properties for constructor params
    def __init__(self, task_ref_name: str, duration_time_seconds: int) -> Self:
        super().__init__(task_ref_name)
        self.input_parameters = {
            "duration": str(duration_time_seconds)
        }


class WaitUntilTask(WaitTask):
    # TODO add properties for constructor params
    def __init__(self, task_ref_name: str, date_time: str) -> Self:
        super().__init__(task_ref_name)
        self.input_parameters = {
            "until": date_time
        }
