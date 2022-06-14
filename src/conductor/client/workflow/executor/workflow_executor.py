from __future__ import annotations
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi


class WorkflowExecutor:
    def __init__(self, configuration: Configuration) -> WorkflowExecutor:
        api_client = ApiClient(configuration)
        self.metadata_client = MetadataResourceApi(api_client)
        self.task_client = TaskResourceApi(api_client)
        self.workflow_client = WorkflowResourceApi(api_client)
