from typing import Optional, List

from src.conductor.client.configuration.configuration import Configuration
from src.conductor.client.http.models import PollData
from src.conductor.client.http.models.task import Task
from src.conductor.client.http.models.task_exec_log import TaskExecLog
from src.conductor.client.http.models.task_result import TaskResult
from src.conductor.client.http.models.task_run import TaskRun
from src.conductor.client.http.models.workflow import Workflow
from src.conductor.client.http.models.workflow_run import WorkflowRun
from src.conductor.client.orkes.orkes_base_client import OrkesBaseClient
from src.conductor.client.task_client import TaskClient


class OrkesTaskClient(OrkesBaseClient, TaskClient):
    def __init__(self, configuration: Configuration):
        super(OrkesTaskClient, self).__init__(configuration)

    def poll_task(self, task_type: str, worker_id: Optional[str] = None, domain: Optional[str] = None) -> Optional[
        Task]:
        kwargs = {}
        if worker_id:
            kwargs.update({"workerid": worker_id})
        if domain:
            kwargs.update({"domain": domain})

        return self.taskResourceApi.poll(task_type, **kwargs)

    def batch_poll_tasks(
            self,
            task_type: str,
            worker_id: Optional[str] = None,
            count: Optional[int] = None,
            timeout_in_millisecond: Optional[int] = None,
            domain: Optional[str] = None
    ) -> List[Task]:
        kwargs = {}
        if worker_id:
            kwargs.update({"workerid": worker_id})
        if count:
            kwargs.update({"count": count})
        if timeout_in_millisecond:
            kwargs.update({"timeout": timeout_in_millisecond})
        if domain:
            kwargs.update({"domain": domain})

        return self.taskResourceApi.batch_poll(task_type, **kwargs)

    def get_task(self, task_id: str) -> Task:
        return self.taskResourceApi.get_task(task_id)

    def update_task(self, task_result: TaskResult) -> str:
        return self.taskResourceApi.update_task(task_result)

    def update_task_by_ref_name(
            self,
            workflow_id: str,
            task_ref_name: str,
            status: str,
            output: object,
            worker_id: Optional[str] = None
    ) -> str:
        body = {"result": output}
        kwargs = {}
        if worker_id:
            kwargs.update({"workerid": worker_id})
        return self.taskResourceApi.update_task1(body, workflow_id, task_ref_name, status, **kwargs)

    def update_task_sync(
            self,
            workflow_id: str,
            task_ref_name: str,
            status: str,
            output: object,
            worker_id: Optional[str] = None
    ) -> Workflow:
        if not isinstance(output, dict):
            output = {'result': output}
        body = output
        kwargs = {}
        if worker_id:
            kwargs.update({"workerid": worker_id})
        return self.taskResourceApi.update_task_sync(body, workflow_id, task_ref_name, status, **kwargs)

    def get_queue_size_for_task(self, task_type: str) -> int:
        queueSizesByTaskType = self.taskResourceApi.size(task_type=[task_type])
        queueSize = queueSizesByTaskType.get(task_type, 0)
        return queueSize

    def add_task_log(self, task_id: str, log_message: str):
        self.taskResourceApi.log(log_message, task_id)

    def get_task_logs(self, task_id: str) -> List[TaskExecLog]:
        return self.taskResourceApi.get_task_logs(task_id)

    def get_task_poll_data(self, task_type: str) -> List[PollData]:
        return self.taskResourceApi.get_poll_data(task_type=task_type)

    def signal_workflow_task_a_sync(
            self,
            workflow_id: str,
            status: str,
            output: object
    ) -> None:
        """
        Signal to a waiting task in a workflow asynchronously

        :param workflow_id: ID of the workflow
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :return: None
        """
        if not isinstance(output, dict):
            output = {'result': output}

        body = output

        self.taskResourceApi.signal_workflow_task_a_sync(body, workflow_id, status)

    def signal_workflow_task_sync(
            self,
            workflow_id: str,
            task_ref_name: str,
            status: str,
            output: object,
            return_strategy: str = "TARGET_WORKFLOW"
    ) -> WorkflowRun | TaskRun:
        """
        Signal to a waiting task in a workflow synchronously

        :param workflow_id: ID of the workflow
        :param task_ref_name: Reference name of the task
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :param return_strategy: Determines what to return (TARGET_WORKFLOW, BLOCKING_WORKFLOW, BLOCKING_TASK, BLOCKING_TASK_INPUT)
        :return: SignalResponse (either WorkflowRun or TaskRun based on return_strategy)
        """
        if not isinstance(output, dict):
            output = {'result': output}

        body = output

        return self.taskResourceApi.signal_workflow_task_sync(
            body=body,
            workflow_id=workflow_id,
            status=status,
            return_strategy=return_strategy
        )

    def signal_workflow_task_with_target_workflow(
            self,
            workflow_id: str,
            status: str,
            output: object
    ) -> WorkflowRun:
        """
        Signal to a waiting task in a workflow synchronously and return the target workflow

        :param workflow_id: ID of the workflow
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :return: WorkflowRun of the target workflow
        """
        if not isinstance(output, dict):
            output = {'result': output}

        body = output

        response = self.taskResourceApi.signal_workflow_task_sync(
            body=body,
            workflow_id=workflow_id,
            status=status,
            return_strategy="TARGET_WORKFLOW"
        )

        return response

    def signal_workflow_task_with_blocking_workflow(
            self,
            workflow_id: str,
            status: str,
            output: object
    ) -> WorkflowRun:
        """
        Signal to a waiting task in a workflow synchronously and return the blocking workflow

        :param workflow_id: ID of the workflow
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :return: WorkflowRun of the blocking workflow
        """
        if not isinstance(output, dict):
            output = {'result': output}

        body = output

        response = self.taskResourceApi.signal_workflow_task_sync(
            body=body,
            workflow_id=workflow_id,
            status=status,
            return_strategy="BLOCKING_WORKFLOW"
        )

        return response

    def signal_workflow_task_with_blocking_task(
            self,
            workflow_id: str,
            status: str,
            output: object
    ) -> TaskRun:
        """
        Signal to a waiting task in a workflow synchronously and return the blocking task

        :param workflow_id: ID of the workflow
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :return: TaskRun of the blocking task
        """
        if not isinstance(output, dict):
            output = {'result': output}

        body = output

        response = self.taskResourceApi.signal_workflow_task_sync(
            body=body,
            workflow_id=workflow_id,
            status=status,
            return_strategy="BLOCKING_TASK"
        )

        return response

    def signal_workflow_task_with_blocking_task_input(
            self,
            workflow_id: str,
            status: str,
            output: object
    ) -> TaskRun:
        """
        Signal to a waiting task in a workflow synchronously and return the blocking task input

        :param workflow_id: ID of the workflow
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :return: TaskRun of the blocking task input
        """
        if not isinstance(output, dict):
            output = {'result': output}

        body = output

        response = self.taskResourceApi.signal_workflow_task_sync(
            body=body,
            workflow_id=workflow_id,
            status=status,
            return_strategy="BLOCKING_TASK_INPUT"
        )

        return response
