from __future__ import annotations
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi
from conductor.client.http.models import *


class WorkflowExecutor:
    def __init__(self, configuration: Configuration) -> WorkflowExecutor:
        api_client = ApiClient(configuration)
        self.metadata_client = MetadataResourceApi(api_client)
        self.task_client = TaskResourceApi(api_client)
        self.workflow_client = WorkflowResourceApi(api_client)

    def register_workflow(self, workflow: WorkflowDef, overwrite: bool) -> object:
        """Create a new workflow definition

        :param WorkflowDef body: (required)
        :param bool overwrite:
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        return self.metadata_client.create(
            body=workflow,
            overwrite=overwrite,
        )

    def start_workflow(self, start_workflow_request: StartWorkflowRequest) -> str:
        """Start a new workflow with StartWorkflowRequest, which allows task to be executed in a domain 

        :param StartWorkflowRequest body: (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        return self.workflow_client.start_workflow(
            body=start_workflow_request,
        )

    def get_workflow(self, workflow_id: str, include_tasks: bool) -> Workflow:
        """Gets the workflow by workflow id

        :param str workflow_id: (required)
        :param bool include_tasks:
        :return: Workflow
                 If the method is called asynchronously,
                 returns the request thread.
        """
        return self.workflow_client.get_execution_status(workflow_id, include_tasks)

    def get_workflow_status(self, workflow_id: str, include_output: bool, include_variables: bool) -> WorkflowStatus:
        """Gets the workflow by workflow id

        :param async_req bool
        :param str workflow_id: (required)
        :param bool include_output:
        :param bool include_variables:
        :return: WorkflowStatus
                 If the method is called asynchronously,
                 returns the request thread.
        """
        return self.workflow_client.get_workflow_status_summary(
            workflow_id,
            include_output,
            include_variables,
        )
