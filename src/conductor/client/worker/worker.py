from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface
from typing import Any, Callable
from typing_extensions import Self
import inspect

ExecuteTaskFunction = Callable[[Task], Any]


def is_callable_input_parameter_a_task(callable: ExecuteTaskFunction, object_type: Any) -> bool:
    parameters = inspect.signature(callable).parameters
    if len(parameters) != 1:
        return False
    parameter = parameters[list(parameters.keys())[0]]
    return parameter.annotation == object_type


def is_callable_return_value_of_type(callable: ExecuteTaskFunction, object_type: Any) -> bool:
    return_annotation = inspect.signature(callable).return_annotation
    return return_annotation == object_type


class Worker(WorkerInterface):
    def __init__(self, task_definition_name: str, execute_function: ExecuteTaskFunction, poll_interval: float = None) -> Self:
        super().__init__(task_definition_name)
        if poll_interval == None:
            poll_interval = super().get_polling_interval_in_seconds()
        self.poll_interval = poll_interval
        self.execute_function = execute_function

    def execute(self, task: Task) -> TaskResult:
        if self._is_execute_function_return_value_a_task_result:
            return self.execute_function(task)
        task_result = self.get_task_result_from_task(task)
        task_result.status = TaskResultStatus.COMPLETED
        task_result.output_data = self.execute_function(task)
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        return self.poll_interval

    @property
    def execute_function(self) -> ExecuteTaskFunction:
        return self._execute_function

    @execute_function.setter
    def execute_function(self, execute_function: ExecuteTaskFunction) -> None:
        self._execute_function = execute_function
        self._is_execute_function_input_parameter_a_task = is_callable_input_parameter_a_task(
            callable=execute_function,
            object_type=Task,
        )
        self._is_execute_function_return_value_a_task_result = is_callable_return_value_of_type(
            callable=execute_function,
            object_type=TaskResult,
        )
