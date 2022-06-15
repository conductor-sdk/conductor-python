from __future__ import annotations
from conductor.client.http.models.workflow_task import WorkflowTask
from conductor.client.workflow.task.task_type import TaskType
from typing import Any, Dict
import abc


class TaskInterface(abc.ABC):
    _name: str
    _task_reference_name: str
    _description: str
    _task_type: TaskType
    _optional: bool
    _input_parameters: Dict[str, Any]

    def __init__(self, task_reference_name: str, task_type: TaskType) -> TaskInterface:
        self._name = task_reference_name
        self._task_reference_name = task_reference_name
        self._task_type = task_type
        self._description = ''
        self._optional = False
        self._input_parameters = {}

    def name(self, name: str) -> TaskInterface:
        if not isinstance(name, str):
            raise Exception('invalid type')
        self._name = name
        return self

    def description(self, description: str) -> TaskInterface:
        if not isinstance(description, str):
            raise Exception('invalid type')
        self._description = description
        return self

    def input(self, input: Dict[str, Any]) -> TaskInterface:
        if not isinstance(input, dict):
            raise Exception('invalid type')
        self._input_parameters = input
        return self

    def optional(self, optional: bool) -> TaskInterface:
        if not isinstance(optional, bool):
            raise Exception('invalid type')
        self._optional = optional
        return self

    def to_workflow_task(self) -> WorkflowTask:
        return WorkflowTask(
            name=self._name,
            task_reference_name=self._task_reference_name,
            workflow_task_type=self._task_type,
            description=self._description,
            input_parameters=self._input_parameters,
            optional=self._optional,
        )

    def output_ref(self, path: str) -> str:
        if path == '':
            return "${%s.output}" % self._task_reference_name
        return "${%s.output.%s}" % self._task_reference_name, path
