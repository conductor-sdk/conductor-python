from ...http.models.workflow_task import WorkflowTask
from .task import TaskInterface
from .task_type import TaskType
from copy import deepcopy
from typing import List
from typing_extensions import Self


class JoinTask(TaskInterface):
    def __init__(self, task_ref_name: str, join_on: List[str] = None) -> Self:
        super().__init__(
            task_reference_name=task_ref_name,
            task_type=TaskType.JOIN
        )
        self._join_on = deepcopy(join_on)

    def to_workflow_task(self) -> WorkflowTask:
        workflow = super().to_workflow_task()
        workflow.join_on = self._join_on
        return workflow
