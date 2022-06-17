from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing_extensions import Self


class StartWorkflowTask(TaskInterface):
    def __init__(self, task_ref_name: str, workflow_name: str, version: int = None, start_workflow_request: StartWorkflowRequest = None) -> Self:
        super().__init__(task_ref_name, TaskType.START_WORKFLOW)
        self._input_parameters = {
            "startWorkflow": {
                "name":          workflow_name,
                "version":       version,
                "input":         start_workflow_request.input,
                "correlationId": start_workflow_request.correlation_id,
            },
        }
