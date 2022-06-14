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
        self._input = {}

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
        self._input = input
        return self

    def to_workflow_task(self) -> WorkflowTask:
        return WorkflowTask(
            name=self.name,
            task_reference_name=self.task_reference_name,
            workflow_task_type=self.task_type,
            description=self.description,
            input_parameters=self.input,
            start_delay=self.start_delay,
            optional=self.optional,
        )
