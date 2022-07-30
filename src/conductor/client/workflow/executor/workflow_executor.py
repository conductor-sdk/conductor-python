from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.metadata_resource_api import MetadataResourceApi
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi
from conductor.client.http.models import *
from typing import Any, Dict, List
from typing_extensions import Self


class WorkflowExecutor:
    def __init__(self, configuration: Configuration) -> Self:
        api_client = ApiClient(configuration)
        self.metadata_client = MetadataResourceApi(api_client)
        self.task_client = TaskResourceApi(api_client)
        self.workflow_client = WorkflowResourceApi(api_client)

    def register_workflow(self, workflow: WorkflowDef, overwrite: bool = None) -> object:
        """Create a new workflow definition

        :param WorkflowDef body:
        :param bool overwrite:
        :return: object
        """
        return self.metadata_client.create(
            body=workflow,
            overwrite=overwrite,
        )

    def start_workflow(self, start_workflow_request: StartWorkflowRequest) -> str:
        """Start a new workflow with StartWorkflowRequest, which allows task to be executed in a domain 

        :param StartWorkflowRequest body:
        :return: str
        """
        return self.workflow_client.start_workflow(
            body=start_workflow_request,
        )

    def start_workflows(self, quantity: int, workflow_name: str) -> List[str]:
        """Start `quantity` instances of given workflow name 

        :param StartWorkflowRequest body:
        :return: str
        """
        workflow_id_list = [''] * quantity
        for i in range(quantity):
            workflow_id_list[i] = self.start_workflow(
                start_workflow_request=StartWorkflowRequest(
                    name=workflow_name
                )
            )
        return workflow_id_list

    def get_workflow(self, workflow_id: str, include_tasks: bool = None) -> Workflow:
        """Gets the workflow by workflow id

        :param str workflow_id:
        :param bool include_tasks:
        :return: Workflow
        """
        return self.workflow_client.get_execution_status(
            workflow_id=workflow_id,
            include_tasks=include_tasks
        )

    def get_workflow_status(self, workflow_id: str, include_output: bool = None, include_variables: bool = None) -> WorkflowStatus:
        """Gets the workflow by workflow id

        :param str workflow_id:
        :param bool include_output:
        :param bool include_variables:
        :return: WorkflowStatus
        """
        return self.workflow_client.get_workflow_status_summary(
            workflow_id=workflow_id,
            include_output=include_output,
            include_variables=include_variables,
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
        """Search for workflows based on payload and other parameters

        :param async_req bool
        :param str query_id:
        :param int start:
        :param int size:
        :param str sort:
        :param str free_text:
        :param str query:
        :param bool skip_cache:
        :return: ScrollableSearchResultWorkflowSummary
        """
        return self.workflow_client.search(
            query_id=query_id,
            start=start,
            size=size,
            sort=sort,
            free_text=free_text,
            query=query,
            skip_cache=skip_cache,
        )

    def get_by_correlation_ids(self, workflow_name: str, correlation_ids: List[str], include_closed: bool = None, include_tasks: bool = None) -> Dict[str, List[WorkflowDef]]:
        """Lists workflows for the given correlation id list

        :param list[str] body:
        :param str name:
        :param bool include_closed:
        :param bool include_tasks:
        :return: dict(str, list[Workflow])
        """
        return self.workflow_client.get_workflows(
            body=correlation_ids,
            name=workflow_name,
            include_closed=include_closed,
            include_tasks=include_tasks,
        )

    def pause(self, workflow_id: str) -> None:
        """Pauses the workflow

        :param str workflow_id:
        :return: None
        """
        return self.workflow_client.pause_workflow1(
            workflow_id=workflow_id
        )

    def resume(self, workflow_id: str) -> None:
        """Resumes the workflow

        :param str workflow_id:
        :return: None
        """
        return self.workflow_client.resume_workflow1(
            workflow_id=workflow_id
        )

    def terminate(self, workflow_id: str, reason: str = None) -> None:
        """Terminate workflow execution

        :param str workflow_id:
        :param str reason:
        :return: None
        """
        return self.workflow_client.terminate1(
            workflow_id=workflow_id,
            reason=reason
        )

    def restart(self, workflow_id: str, use_latest_definitions: bool = None) -> None:
        """Restarts a completed workflow

        :param str workflow_id:
        :param bool use_latest_definitions:
        :return: None
        """
        return self.workflow_client.restart1(
            workflow_id=workflow_id,
            use_latest_definitions=use_latest_definitions
        )

    def retry(self, workflow_id: str, resume_subworkflow_tasks: bool = None) -> None:
        """Retries the last failed task  

        :param str workflow_id:
        :param bool resume_subworkflow_tasks:
        :return: None
        """
        return self.workflow_client.retry1(
            workflow_id=workflow_id,
            resume_subworkflow_tasks=resume_subworkflow_tasks
        )

    def rerun(self, rerun_workflow_request: RerunWorkflowRequest, workflow_id: str) -> str:
        """Reruns the workflow from a specific task

        :param RerunWorkflowRequest body:
        :param str workflow_id:
        :return: str
        """
        return self.workflow_client.rerun(
            body=rerun_workflow_request,
            workflow_id=workflow_id,
        )

    def skip_task_from_workflow(self, workflow_id: str, task_reference_name: str, skip_task_request: SkipTaskRequest = None) -> None:
        """Skips a given task from a current running workflow

        :param str workflow_id:
        :param str task_reference_name:
        :param SkipTaskRequest body:
        :return: None
        """
        return self.workflow_client.skip_task_from_workflow(
            workflow_id=workflow_id,
            task_reference_name=task_reference_name,
            body=skip_task_request,
        )

    def update_task(self, task_id: str, workflow_id: str, task_output: Dict[str, Any], status: str) -> str:
        """Update a task

        :param TaskResult body:
        :return: str
        """
        task_result = self.__get_task_result(
            task_id, workflow_id, task_output, status
        )
        return self.task_client.update_task(
            body=task_result,
        )

    def update_task_by_ref_name(self, task_output: Dict[str, Any], workflow_id: str, task_reference_name: str, status: str) -> str:
        """Update a task By Ref Name  

        :param dict(str, object) body:
        :param str workflow_id:
        :param str task_ref_name:
        :param str status:
        :return: str
        """
        return self.task_client.update_task1(
            body=task_output,
            workflow_id=workflow_id,
            task_ref_name=task_reference_name,
            status=status,
        )

    def get_task(self, task_id: str) -> str:
        """Get task by Id 

        :param str task_id:
        :return: Task
        """
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
