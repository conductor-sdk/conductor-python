from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.worker.worker_interface import WorkerInterface
from typing import Any, Callable
from typing_extensions import Self
import inspect

ExecuteTaskFunction = Callable[[Any], Any]


def is_callable_input_parameter_a_task(execute_function: ExecuteTaskFunction) -> bool:
    parameters = inspect.signature(execute_function).parameters
    if len(parameters) != 1:
        return False
    parameter = parameters[list(parameters.keys())[0]]
    return parameter.annotation == Task


def is_callable_return_value_a_task_result(execute_function: ExecuteTaskFunction) -> bool:
    return_annotation = inspect.signature(execute_function).return_annotation
    return return_annotation == TaskResult


class Worker(WorkerInterface):
    def __init__(self, task_definition_name: str, execute_function: ExecuteTaskFunction,  poll_interval: float) -> Self:
        super().__init__(task_definition_name)
        self.poll_interval = poll_interval
        self.execute_function = execute_function

    def execute(self, task: Task) -> TaskResult:
        return self.execute_function(task)

    def get_polling_interval_in_seconds(self) -> float:
        return self.poll_interval

    @property
    def execute_function(self) -> ExecuteTaskFunction:
        return self._execute_function

    @execute_function.setter
    def execute_function(self, execute_function: ExecuteTaskFunction) -> None:
        self._execute_function = execute_function
        self._is_execute_function_input_parameter_a_task = is_callable_input_parameter_a_task(
            execute_function
        )
        self._is_execute_function_return_value_a_task_result = is_callable_return_value_a_task_result(
            execute_function
        )
