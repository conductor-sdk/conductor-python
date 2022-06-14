from __future__ import annotations
from typing import Any
from src.conductor.client.workflow.task_type import TaskType
from src.conductor.client.http.models.workflow_task import WorkflowTask
import abc


class TaskInterface(abc.ABC):
    def __init__(self, task_reference_name: str, task_type: TaskType) -> TaskInterface:
        self._name = task_reference_name
        self.task_reference_name = task_reference_name
        self.task_type = task_type
        self.description = ''
        self.optional = False
        self.start_delay = None
        self.input = {}

    def Name(self, name: str) -> TaskInterface:
        self.name = name
        return self

    def Description(self, description: str) -> TaskInterface:
        self.description = description
        return self

    def Input(self, input: Any) -> TaskInterface:
        self.input = input
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
