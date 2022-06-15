from __future__ import annotations
from typing import List
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.http.models.workflow_task import WorkflowTask
from task import TaskInterface


class JoinTask(TaskInterface):
    _join_on: List[str]

    def __init__(self, task_ref_name: str, join_on: List[str]) -> JoinTask:
        super().__init__(task_ref_name, TaskType.JOIN)
        self._join_on = join_on

    def to_workflow_task(self) -> WorkflowTask:
        workflow = super().to_workflow_task()
        workflow.join_on = self._join_on
        return workflow
