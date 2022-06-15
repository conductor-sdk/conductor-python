from __future__ import annotations
from conductor.client.workflow.task.task_type import TaskType
from conductor.client.http.models.workflow_task import WorkflowTask
from conductor.client.workflow.task.task import TaskInterface


class DynamicTask(TaskInterface):
    DYNAMIC_TASK_PARAM = 'taskToExecute'

    def __init__(self, task_ref_name: str, task_name_parameter: str) -> DynamicTask:
        super().__init__(task_ref_name, TaskType.DYNAMIC)
        self._input_parameters = {
            DynamicTask.DYNAMIC_TASK_PARAM: task_name_parameter,
        }

    def to_workflow_task(self) -> WorkflowTask:
        workflow = super().to_workflow_task()
        workflow.dynamic_task_name_param = DynamicTask.DYNAMIC_TASK_PARAM
