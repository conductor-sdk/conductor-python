from __future__ import annotations
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi
from conductor.client.http.models.start_workflow_request import StartWorkflowRequest
from conductor.client.http.models import *


class WorkflowExecutor:
    def __init__(self, configuration: Configuration) -> WorkflowExecutor:
        api_client = ApiClient(configuration)
        self.metadata_client = MetadataResourceApi(api_client)
        self.task_client = TaskResourceApi(api_client)
        self.workflow_client = WorkflowResourceApi(api_client)

    def register_workflow(self, overwrite: bool, workflow):
        # TODO parse response
        # TODO add overwrite to request
        return self.metadata_client.create(workflow)

    def start_workflow(self, start_workflow_request: StartWorkflowRequest):
        # TODO parse response
        return self.workflow_client.start_workflow1(start_workflow_request)

    def get_workflow(self, workflow_id: str, include_tasks: bool) -> Workflow:
        # TODO parse response
        # TODO add include_tasks to request
        return self.workflow_client.get_execution_status(workflow_id)

    # TODO add return type guide
    def get_workflow_status(self, workflow_id: str, include_output: bool, include_variables: bool):
        # TODO add call to new get workflow status api
        # TODO parse response
        pass

    # TODO add remaining methods, equivalent here: https://github.dev/conductor-sdk/conductor-go/blob/main/sdk/workflow/executor/executor.go
