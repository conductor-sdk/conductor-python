import dataclasses
import inspect
import logging
import time
import traceback
from copy import deepcopy
from typing import Any, Callable, Union

from typing_extensions import Self

from conductor.client.automator import utils
from conductor.client.automator.utils import convert
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient
from conductor.client.http.models import TaskExecLog
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

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


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
        self.api_client = ApiClient()
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
        task_input = {}

        if self._is_execute_function_input_parameter_a_task:
            task_input = task
        else:
            params = inspect.signature(self.execute_function).parameters
            for input_name in params:
                logger.info(f'{input_name} param type is {params[input_name].annotation}')
                typ = params[input_name].annotation
                if input_name in task.input_data:
                    logger.info(
                        f'input name is {input_name} and task inputs are {task.input_data} and input type is {type(task.input_data)}')
                    if typ in utils.simple_types:
                        task_input[input_name] = task.input_data[input_name]
                    else:
                        task_input[input_name] = convert(typ, task.input_data[input_name])

        task_result: TaskResult = self.get_task_result_from_task(task)
        try:
            output = self.execute_function(**task_input)

            if type(output) == TaskResult:
                output.task_id = task.task_id
                output.workflow_instance_id = task.workflow_instance_id
                return output

            else:

                task_result.status = TaskResultStatus.COMPLETED
                task_result.output_data = output

        except NonRetryableException as ne:
            task_result.status = TaskResultStatus.FAILED_WITH_TERMINAL_ERROR
            if len(ne.args) > 0:
                task_result.reason_for_incompletion = ne.args[0]

        except Exception as ne:
            logger.error(
                f'Error executing task {task.task_def_name} with id {task.task_id}.  error = {traceback.format_exc()}')

            task_result.logs = [TaskExecLog(
                traceback.format_exc(), task_result.task_id, int(time.time()))]
            task_result.status = TaskResultStatus.FAILED
            if len(ne.args) > 0:
                task_result.reason_for_incompletion = ne.args[0]

        if dataclasses.is_dataclass(type(task_result.output_data)):
            output = dataclasses.asdict(task_result.output_data)
            task_result.output_data = output
            return task_result
        if not isinstance(task_result.output_data, dict):
            output = task_result.output_data
            task_result.output_data = self.api_client.sanitize_for_serialization(output)
            if not isinstance(task_result.output_data, dict):
                task_result.output_data = {'result': task_result.output_data}

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
