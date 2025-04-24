from abc import ABC, abstractmethod
from typing import Optional, List

from conductor.client.http.models import PollData, WorkflowRun
from src.conductor.client.http.models.signal_response import SignalResponse
from src.conductor.client.http.models.task_run import TaskRun
from conductor.client.http.models.workflow import Workflow
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.http.models.task_exec_log import TaskExecLog


class TaskClient(ABC):
    @abstractmethod
    def poll_task(self, task_type: str, worker_id: Optional[str] = None, domain: Optional[str] = None) -> Optional[Task]:
        pass

    @abstractmethod
    def batch_poll_tasks(
            self,
            task_type: str,
            worker_id: Optional[str] = None,
            count: Optional[int] = None,
            timeout_in_millisecond: Optional[int] = None,
            domain: Optional[str] = None
    ) -> List[Task]:
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def update_task(self, task_result: TaskResult) -> str:
        pass

    @abstractmethod
    def update_task_by_ref_name(
            self,
            workflow_id: str,
            task_ref_name: str,
            status: TaskResultStatus,
            output: object,
            worker_id: Optional[str] = None
    ) -> str:
        pass

    @abstractmethod
    def update_task_sync(
            self,
            workflow_id: str,
            task_ref_name: str,
            status: TaskResultStatus,
            output: object,
            worker_id: Optional[str] = None
    ) -> Workflow:
        pass

    @abstractmethod
    def get_queue_size_for_task(self, task_type: str) -> int:
        pass

    @abstractmethod
    def add_task_log(self, task_id: str, log_message: str):
        pass

    @abstractmethod
    def get_task_logs(self, task_id: str) -> List[TaskExecLog]:
        pass

    @abstractmethod
    def get_task_poll_data(self, task_type: str) -> List[PollData]:
        pass

    @abstractmethod
    def signal_workflow_task_a_sync(
            self,
            workflow_id: str,
            status: str,
            output: object
    ) -> None:
        """
        Signal to a waiting task in a workflow asynchronously

        :param workflow_id: ID of the workflow
        :param task_ref_name: Reference name of the task
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :return: None
        """
        pass

    @abstractmethod
    def signal_workflow_task_sync(
            self,
            workflow_id: str,
            task_ref_name: str,
            status: str,
            output: object,
            return_strategy: str = "TARGET_WORKFLOW"
    ) -> SignalResponse:
        """
        Signal to a waiting task in a workflow synchronously

        :param workflow_id: ID of the workflow
        :param task_ref_name: Reference name of the task
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :param return_strategy: Determines what to return (TARGET_WORKFLOW, BLOCKING_WORKFLOW, BLOCKING_TASK, BLOCKING_TASK_INPUT)
        :return: SignalResponse (either WorkflowRun or TaskRun based on return_strategy)
        """
        pass

    @abstractmethod
    def signal_workflow_task_with_target_workflow(
            self,
            workflow_id: str,
            task_ref_name: str,
            status: str,
            output: object
    ) -> WorkflowRun:
        """
        Signal to a waiting task in a workflow synchronously and return the target workflow

        :param workflow_id: ID of the workflow
        :param task_ref_name: Reference name of the task
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :return: WorkflowRun of the target workflow
        """
        pass

    @abstractmethod
    def signal_workflow_task_with_blocking_workflow(
            self,
            workflow_id: str,
            task_ref_name: str,
            status: str,
            output: object
    ) -> WorkflowRun:
        """
        Signal to a waiting task in a workflow synchronously and return the blocking workflow

        :param workflow_id: ID of the workflow
        :param task_ref_name: Reference name of the task
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :return: WorkflowRun of the blocking workflow
        """
        pass

    @abstractmethod
    def signal_workflow_task_with_blocking_task(
            self,
            workflow_id: str,
            status: str,
            output: object
    ) -> TaskRun:
        """
        Signal to a waiting task in a workflow synchronously and return the blocking task

        :param workflow_id: ID of the workflow
        :param task_ref_name: Reference name of the task
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :return: TaskRun of the blocking task
        """
        pass

    @abstractmethod
    def signal_workflow_task_with_blocking_task_input(
            self,
            workflow_id: str,
            task_ref_name: str,
            status: str,
            output: object
    ) -> TaskRun:
        """
        Signal to a waiting task in a workflow synchronously and return the blocking task input

        :param workflow_id: ID of the workflow
        :param task_ref_name: Reference name of the task
        :param status: Status to set for the task (e.g. COMPLETED, FAILED)
        :param output: Output data for the task
        :return: TaskRun of the blocking task input
        """
        pass