from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Dict, List

from typing_extensions import Self

from conductor.client.http.models.workflow_task import WorkflowTask
from conductor.client.workflow.task.task_type import TaskType


def get_task_interface_list_as_workflow_task_list(*tasks: Self) -> List[WorkflowTask]:
    converted_tasks = []
    for task in tasks:
        converted_tasks.append(task.to_workflow_task())
    return converted_tasks


class TaskInterface(ABC):
    @abstractmethod
    def __init__(self,
                 task_reference_name: str,
                 task_type: TaskType,
                 task_name: str = None,
                 description: str = None,
                 optional: bool = None,
                 input_parameters: Dict[str, Any] = None) -> Self:
        self.task_reference_name = task_reference_name
        self.task_type = task_type
        self.name = task_name or task_reference_name
        self.description = description
        self.optional = optional
        self.input_parameters = input_parameters

    @property
    def task_reference_name(self) -> str:
        return self._task_reference_name

    @task_reference_name.setter
    def task_reference_name(self, task_reference_name: str) -> None:
        if not isinstance(task_reference_name, str):
            raise Exception('invalid type')
        self._task_reference_name = deepcopy(task_reference_name)

    @property
    def task_type(self) -> TaskType:
        return self._task_type

    @task_type.setter
    def task_type(self, task_type: TaskType) -> None:
        if not isinstance(task_type, TaskType):
            raise Exception('invalid type')
        self._task_type = deepcopy(task_type)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if not isinstance(name, str):
            raise Exception('invalid type')
        self._name = name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        if description != None and not isinstance(description, str):
            raise Exception('invalid type')
        self._description = deepcopy(description)

    @property
    def optional(self) -> bool:
        return self._optional

    @optional.setter
    def optional(self, optional: bool) -> None:
        if optional != None and not isinstance(optional, bool):
            raise Exception('invalid type')
        self._optional = deepcopy(optional)

    @property
    def input_parameters(self) -> Dict[str, Any]:
        return self._input_parameters

    @input_parameters.setter
    def input_parameters(self, input_parameters: Dict[str, Any]) -> None:
        if input_parameters is None:
            self._input_parameters = {}
            return
        if not isinstance(input_parameters, dict):
            try:
                self._input_parameters = input_parameters.__dict__
            except:
                raise Exception(f'invalid type: {type(input_parameters)}')
        self._input_parameters = deepcopy(input_parameters)

    def input(self, key: str, value: Any) -> Self:
        if not isinstance(key, str):
            raise Exception('invalid type')
        self._input_parameters[key] = deepcopy(value)
        return self

    def to_workflow_task(self) -> WorkflowTask:
        return WorkflowTask(
            name=self._name,
            task_reference_name=self._task_reference_name,
            type=self._task_type.value,
            description=self._description,
            input_parameters=self._input_parameters,
            optional=self._optional,
        )

    def output_ref(self, path: str) -> str:
        if path == '':
            return f'${{{self._task_reference_name}.output}}'
        return f'${{{self._task_reference_name}.output.{path}}}'

    def __getattribute__(self, __name: str) -> Any:
        try:
            val = super().__getattribute__(__name)
            return val
        except AttributeError as ae:
            if not __name.startswith('_'):
                return '${' + self.task_reference_name + '.output.' + __name + '}'
            raise ae
