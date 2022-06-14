from __future__ import annotations
from src.conductor.client.http.models.workflow_task import WorkflowTask
from src.conductor.client.workflow.task import TaskInterface
from src.conductor.client.workflow.task_type import TaskType
import abc


class EventTaskInterface(TaskInterface, abc.ABC):
    _sink: str

    def __init__(self, task_ref_name: str, event_prefix: str, event_suffix: str) -> EventTaskInterface:
        task = super().__init__(task_ref_name, TaskType.EVENT)
        task._sink = event_prefix + ':' + event_suffix
        return task

    def to_workflow_task(self) -> WorkflowTask:
        workflow_task = super().to_workflow_task()
        workflow_task.sink = self._sink
        return workflow_task


class SqsEventTask(EventTaskInterface):
    def __init__(self, task_ref_name: str, queue_name: str) -> SqsEventTask:
        super().__init__(task_ref_name, 'sqs', queue_name)


class ConductorEventTask(EventTaskInterface):
    def __init__(self, task_ref_name: str, event_name: str) -> SqsEventTask:
        super().__init__(task_ref_name, 'conductor', event_name)
