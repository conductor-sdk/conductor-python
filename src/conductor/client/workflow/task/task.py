from abc import ABC
from conductor.client.http.models.workflow_task import WorkflowTask
from conductor.client.workflow.task.task_type import TaskType
from typing import Any, Dict, List
from typing_extensions import Self


def get_task_interface_list_as_workflow_task_list(*tasks: Self) -> List[WorkflowTask]:
    converted_tasks = []
    for task in tasks:
        converted_tasks.append(task.to_workflow_task())
    return converted_tasks


class TaskInterface(ABC):
    _task_reference_name: str
    _task_type: TaskType
    _name: str
    _description: str
    _optional: bool
    _input_parameters: Dict[str, Any]

    def __init__(self,
                 task_reference_name: str,
                 task_type: TaskType,
                 task_def_name: str = None,
                 description: str = None,
                 optional: bool = False,
                 input_parameters: Dict[str, Any] = {}) -> Self:
        self._task_reference_name = task_reference_name
        self._task_type = task_type
        if task_def_name == None:
            task_def_name = task_reference_name
        self.name = task_def_name
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
        self._task_reference_name = task_reference_name

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
        self._description = description

    @property
    def optional(self) -> bool:
        return self._optional

    @optional.setter
    def optional(self, optional: bool) -> None:
        if not isinstance(optional, bool):
            raise Exception('invalid type')
        self._optional = optional

    @property
    def input_parameters(self) -> Dict[str, Any]:
        return self._input_parameters

    @input_parameters.setter
    def input_parameters(self, input_parameters: Dict[str, Any]) -> None:
        if not isinstance(input_parameters, dict):
            raise Exception('invalid type')
        for key in input_parameters.keys():
            if not isinstance(key, str):
                raise Exception('invalid type')
        self._input_parameters = input_parameters

    def input(self, key: str, value: Any) -> Self:
        if not isinstance(key, str):
            raise Exception('invalid type')
        self._input_parameters[key] = value
        return self

    def to_workflow_task(self) -> WorkflowTask:
        return WorkflowTask(
            name=self._name,
            task_reference_name=self._task_reference_name,
            workflow_task_type=self._task_type.value,
            description=self._description,
            input_parameters=self._input_parameters,
            optional=self._optional,
        )

    def output_ref(self, path: str) -> str:
        if path == '':
            return "${%s.output}" % self._task_reference_name
        return "${%s.output.%s}" % self._task_reference_name, path
