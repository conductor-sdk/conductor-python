from copy import deepcopy
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface
from typing import Any, Callable, Union
from typing_extensions import Self
import inspect

ExecuteTaskFunction = Callable[
    [
        Union[Task, object]
    ],
    Union[TaskResult, object]
]


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
    def __init__(self,
                 task_definition_names: str,
                 execute_function: ExecuteTaskFunction,
                 poll_interval: float = None,
                 domain: str = None,
                 worker_id: str = None,
                 ) -> Self:
        super().__init__(task_definition_names)
        if poll_interval == None:
            self.poll_interval = deepcopy(
                super().get_polling_interval_in_seconds())
        else:
            self.poll_interval = deepcopy(poll_interval)
        self.domain = deepcopy(domain)
        if worker_id is None:
            self.worker_id = deepcopy(super().get_identity())
        else:
            self.worker_id = deepcopy(worker_id)
        self.execute_function = deepcopy(execute_function)

    def execute(self, task: Task) -> TaskResult:
        execute_function_input = None
        if self._is_execute_function_input_parameter_a_task:
            execute_function_input = task
        else:
            execute_function_input = task.input_data
        if self._is_execute_function_return_value_a_task_result:
            execute_function_output = self.execute_function(
                execute_function_input)
            if type(execute_function_output) == TaskResult:
                execute_function_output.task_id = task.task_id
                execute_function_output.workflow_instance_id = task.workflow_instance_id
            return execute_function_output
        task_result = self.get_task_result_from_task(task)
        task_result.status = TaskResultStatus.COMPLETED
        task_result.output_data = self.execute_function(task)
        return task_result

    def get_identity(self) -> str:
        return self.worker_id

    def get_polling_interval_in_seconds(self) -> float:
        return self.poll_interval

    def get_domain(self) -> str:
        return self.domain

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
