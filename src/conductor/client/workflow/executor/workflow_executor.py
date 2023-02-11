from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi
from conductor.client.http.models.correlation_ids_search_request import CorrelationIdsSearchRequest
from conductor.client.http.models import *
from typing import Any, Dict, List
from typing_extensions import Self
import uuid

class WorkflowExecutor:
    def __init__(self, configuration: Configuration) -> Self:
        api_client = ApiClient(configuration)
        self.metadata_client = MetadataResourceApi(api_client)
        self.task_client = TaskResourceApi(api_client)
        self.workflow_client = WorkflowResourceApi(api_client)

    def register_workflow(self, workflow: WorkflowDef, overwrite: bool = None) -> object:
        """Create a new workflow definition"""
        kwargs = {}
        if overwrite is not None:
            kwargs['overwrite'] = overwrite
        return self.metadata_client.create(
            body=workflow, **kwargs
        )

    def start_workflow(self, start_workflow_request: StartWorkflowRequest) -> str:
        """Start a new workflow with StartWorkflowRequest, which allows task to be executed in a domain """
        return self.workflow_client.start_workflow(
            body=start_workflow_request,
        )

    def start_workflows(self, *start_workflow_request: StartWorkflowRequest) -> List[str]:
        """Start multiple instances of workflows.  Note, there is no parallelism implemented in starting so giving a
        very large number can impact the latencies and performance
        """
        workflow_id_list = [''] * len(start_workflow_request)
        for i in range(len(start_workflow_request)):
            workflow_id_list[i] = self.start_workflow(
                start_workflow_request=start_workflow_request[i]
            )
        return workflow_id_list

    def execute_workflow(self, request: StartWorkflowRequest, wait_until_task_ref: str) -> WorkflowRun:
        """Executes a workflow with StartWorkflowRequest and waits for the completion of the workflow or until a
        specific task in the workflow """
        return self.workflow_client.execute_workflow(
            body=request,
            request_id=str(uuid.uuid4()),
            version=request.version,
            name=request.name,
            wait_until_task_ref=wait_until_task_ref,
        )

    def remove_workflow(self, workflow_id: str, archive_workflow: bool = None) -> None:
        """Removes the workflow permanently from the system"""
        kwargs = {}
        if archive_workflow is not None:
            kwargs['archive_workflow'] = archive_workflow
        return self.workflow_client.delete(
            workflow_id=workflow_id, **kwargs
        )

    def get_workflow(self, workflow_id: str, include_tasks: bool = None) -> Workflow:
        """Gets the workflow by workflow id"""
        kwargs = {}
        if include_tasks is not None:
            kwargs['include_tasks'] = include_tasks
        return self.workflow_client.get_execution_status(
            workflow_id=workflow_id, **kwargs
        )

    def get_workflow_status(self, workflow_id: str, include_output: bool = None, include_variables: bool = None) -> WorkflowStatus:
        """Gets the workflow by workflow id"""
        kwargs = {}
        if include_output is not None:
            kwargs['include_output'] = include_output
        if include_variables is not None:
            kwargs['include_variables'] = include_variables
        return self.workflow_client.get_workflow_status_summary(
            workflow_id=workflow_id, **kwargs
        )

    def search(
        self,
        query_id: str = None,
        start: int = None,
        size: int = None,
        sort: str = None,
        free_text: str = None,
        query: str = None,
        skip_cache: bool = None,
    ) -> ScrollableSearchResultWorkflowSummary:
        """Search for workflows based on payload and other parameters"""
        kwargs = {}
        if query_id is not None:
            kwargs['query_id'] = query_id
        if start is not None:
            kwargs['start'] = start
        if size is not None:
            kwargs['size'] = size
        if sort is not None:
            kwargs['sort'] = sort
        if free_text is not None:
            kwargs['free_text'] = free_text
        if query is not None:
            kwargs['query'] = query
        if skip_cache is not None:
            kwargs['skip_cache'] = skip_cache
        return self.workflow_client.search(**kwargs)

    def get_by_correlation_ids(
        self,
        workflow_name: str,
        correlation_ids: List[str],
        include_closed: bool = None,
        include_tasks: bool = None
    ) -> Dict[str, List[WorkflowDef]]:
        """Lists workflows for the given correlation id list"""
        kwargs = {}
        if include_closed is not None:
            kwargs['include_closed'] = include_closed
        if include_tasks is not None:
            kwargs['include_tasks'] = include_tasks
        return self.workflow_client.get_workflows(
            body=correlation_ids,
            name=workflow_name,
            **kwargs
        )

    def get_by_correlation_ids_and_names(self, body: CorrelationIdsSearchRequest, include_closed: bool = None, include_tasks: bool = None) -> Dict[str, List[Workflow]]:
        """Given the list of correlation ids and list of workflow names, find and return workflows
        Returns a map with key as correlationId and value as a list of Workflows
        When IncludeClosed is set to true, the return value also includes workflows that are completed otherwise only running workflows are returned"""
        args = {'body': body}
        if include_closed != None:
            args['include_closed'] = True
        if include_tasks != None:
            args['include_tasks'] = True
        return self.workflow_client.get_workflows_batch(**args)

    def pause(self, workflow_id: str) -> None:
        """Pauses the workflow"""
        return self.workflow_client.pause_workflow1(
            workflow_id=workflow_id
        )

    def resume(self, workflow_id: str) -> None:
        """Resumes the workflow"""
        return self.workflow_client.resume_workflow1(
            workflow_id=workflow_id
        )

    def terminate(self, workflow_id: str, reason: str = None, trigger_failure_workflow: bool = None) -> None:
        """Terminate workflow execution"""
        kwargs = {}
        if reason is not None:
            kwargs['reason'] = reason
        if trigger_failure_workflow is not None:
            kwargs['triggerFailureWorkflow'] = trigger_failure_workflow
        return self.workflow_client.terminate1(
            workflow_id=workflow_id,
            **kwargs
        )

    def restart(self, workflow_id: str, use_latest_definitions: bool = None) -> None:
        """Restarts a completed workflow"""
        kwargs = {}
        if use_latest_definitions is not None:
            kwargs['use_latest_definitions'] = use_latest_definitions
        return self.workflow_client.restart1(
            workflow_id=workflow_id, **kwargs
        )

    def retry(self, workflow_id: str, resume_subworkflow_tasks: bool = None) -> None:
        """Retries the last failed task"""
        kwargs = {}
        if resume_subworkflow_tasks is not None:
            kwargs['resume_subworkflow_tasks'] = resume_subworkflow_tasks
        return self.workflow_client.retry1(
            workflow_id=workflow_id, **kwargs
        )

    def rerun(self, rerun_workflow_request: RerunWorkflowRequest, workflow_id: str) -> str:
        """Reruns the workflow from a specific task"""
        return self.workflow_client.rerun(
            body=rerun_workflow_request,
            workflow_id=workflow_id,
        )

    def skip_task_from_workflow(self, workflow_id: str, task_reference_name: str, skip_task_request: SkipTaskRequest = None) -> None:
        """Skips a given task from a current running workflow"""
        kwargs = {}
        if skip_task_request is not None:
            kwargs['body'] = skip_task_request
        return self.workflow_client.skip_task_from_workflow(
            workflow_id=workflow_id,
            task_reference_name=task_reference_name,
            **kwargs
        )

    def update_task(self, task_id: str, workflow_id: str, task_output: Dict[str, Any], status: str) -> str:
        """Update a task"""
        task_result = self.__get_task_result(
            task_id, workflow_id, task_output, status
        )
        return self.task_client.update_task(
            body=task_result,
        )

    def update_task_by_ref_name(self, task_output: Dict[str, Any], workflow_id: str, task_reference_name: str, status: str) -> str:
        """Update a task By Ref Name"""
        return self.task_client.update_task1(
            body=task_output,
            workflow_id=workflow_id,
            task_ref_name=task_reference_name,
            status=status,
        )

    def get_task(self, task_id: str) -> str:
        """Get task by Id"""
        return self.task_client.get_task(
            task_id=task_id
        )

    def __get_task_result(self, task_id: str, workflow_id: str, task_output: Dict[str, Any], status: str) -> TaskResult:
        return TaskResult(
            workflow_instance_id=workflow_id,
            task_id=task_id,
            output_data=task_output,
            status=status
        )
