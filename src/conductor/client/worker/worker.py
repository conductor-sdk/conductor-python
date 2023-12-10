import inspect
from copy import deepcopy
from typing import Any, Callable, Union

from typing_extensions import Self

from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.exception import NonRetryableException
from conductor.client.worker.worker_interface import WorkerInterface, DEFAULT_POLLING_INTERVAL

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
    return parameter.annotation == object_type or parameter.annotation == parameter.empty or parameter.annotation == object


def is_callable_return_value_of_type(callable: ExecuteTaskFunction, object_type: Any) -> bool:
    return_annotation = inspect.signature(callable).return_annotation
    return return_annotation == object_type


class Worker(WorkerInterface):
    def __init__(self,
                 task_definition_name: str,
                 execute_function: ExecuteTaskFunction,
                 poll_interval: float = None,
                 domain: str = None,
                 worker_id: str = None,
                 ) -> Self:
        super().__init__(task_definition_name)
        if poll_interval is None:
            self.poll_interval = DEFAULT_POLLING_INTERVAL
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
            execute_function_input = {}

            for input_name in inspect.signature(self.execute_function).parameters:
                if input_name in task.input_data:
                    execute_function_input[input_name] = task.input_data[input_name]
        if self._is_execute_function_return_value_a_task_result:
            execute_function_output = self.execute_function(execute_function_input)
            if type(execute_function_output) == TaskResult:
                execute_function_output.task_id = task.task_id
                execute_function_output.workflow_instance_id = task.workflow_instance_id
            return execute_function_output
        task_result = self.get_task_result_from_task(task)
        task_result.status = TaskResultStatus.COMPLETED
        if self._is_execute_function_input_parameter_a_task:
            task_result.output_data = self.execute_function(task)
        else:
            try:
                task_result.output_data = self.execute_function(**execute_function_input)
            except NonRetryableException as ne:
                task_result.status = TaskResultStatus.FAILED_WITH_TERMINAL_ERROR
                if len(ne.args) > 0:
                    task_result.reason_for_incompletion = ne.args[0]
            except Exception as ne:
                task_result.status = TaskResultStatus.FAILED
                if len(ne.args) > 0:
                    task_result.reason_for_incompletion = ne.args[0]
        if not isinstance(task_result.output_data, dict):
            output = task_result.output_data
            task_result.output_data = {'result': output}
        return task_result

    def get_identity(self) -> str:
        return self.worker_id

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
