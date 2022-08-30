from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface
from copy import deepcopy
from typing import Any, Callable, Union
from typing_extensions import Self
import inspect

WorkerInput = Union[Task, Any]
WorkerOutput = Union[TaskResult, Any]
WorkerExecutionFunction = Callable[[WorkerInput], WorkerOutput]


def is_callable_input_parameter_of_type(callable: WorkerExecutionFunction, object_type: Any) -> bool:
    parameters = inspect.signature(callable).parameters
    if len(parameters) != 1:
        return False
    parameter = parameters[list(parameters.keys())[0]]
    return parameter.annotation == object_type


def is_callable_return_value_of_type(callable: WorkerExecutionFunction, object_type: Any) -> bool:
    return_annotation = inspect.signature(callable).return_annotation
    return return_annotation == object_type


class Worker(WorkerInterface):
    def __init__(
        self,
        task_definition_name: str,
        worker_execution_function: WorkerExecutionFunction,
        poll_interval: float = None,
        domain: str = None,
    ) -> Self:
        super().__init__(task_definition_name)
        if poll_interval == None:
            self.poll_interval = super().get_polling_interval_in_seconds()
        else:
            self.poll_interval = deepcopy(poll_interval)
        if domain == None:
            self.domain = super().get_domain()
        else:
            self.domain = deepcopy(domain)
        self.worker_execution_function = deepcopy(worker_execution_function)

    def execute(self, task: Task) -> TaskResult:
        worker_execution_function_input = None
        if self._is_worker_execution_function_input_parameter_a_task:
            worker_execution_function_input = task
        else:
            worker_execution_function_input = task.input_data
        if self._is_worker_execution_function_return_value_a_task_result:
            worker_execution_function_output = self.worker_execution_function(
                worker_execution_function_input)
            if type(worker_execution_function_output) == TaskResult:
                worker_execution_function_output.task_id = task.task_id
                worker_execution_function_output.workflow_instance_id = task.workflow_instance_id
            return worker_execution_function_output
        task_result = self.get_task_result_from_task(task)
        task_result.status = TaskResultStatus.COMPLETED
        task_result.output_data = self.worker_execution_function(task)
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        return self.poll_interval

    def get_domain(self) -> str:
        return self.domain

    @property
    def worker_execution_function(self) -> WorkerExecutionFunction:
        return self._worker_execution_function

    @worker_execution_function.setter
    def worker_execution_function(self, worker_execution_function: WorkerExecutionFunction) -> None:
        self._worker_execution_function = worker_execution_function
        self._is_worker_execution_function_input_parameter_a_task = is_callable_input_parameter_of_type(
            callable=worker_execution_function,
            object_type=Task,
        )
        self._is_worker_execution_function_return_value_a_task_result = is_callable_return_value_of_type(
            callable=worker_execution_function,
            object_type=TaskResult,
        )
