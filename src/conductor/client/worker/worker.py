from typing import Callable
from typing_extensions import Self
from conductor.client.worker.worker_interface import WorkerInterface
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult

ExecuteTaskFunction = Callable[[Task], TaskResult]


class Worker(WorkerInterface):
    def __init__(self, task_definition_name: str, execute_function: ExecuteTaskFunction,  poll_interval: float) -> Self:
        super().__init__(task_definition_name)
        self.execute_function = execute_function
        self.poll_interval = poll_interval

    def execute(self, task: Task) -> TaskResult:
        return self.execute_function(task)

    def get_polling_interval_in_seconds(self) -> float:
        return self.poll_interval
