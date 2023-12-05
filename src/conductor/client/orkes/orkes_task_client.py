"""Orkes Task Client

The class in this module is allowed to manage the life cycle of a task.
"""

from typing import List, Optional

from conductor.client.exceptions.api_exception_handler import (
    api_exception_handler, for_all_methods)
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_exec_log import TaskExecLog
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.workflow import Workflow
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.task_client import TaskClient


@for_all_methods(api_exception_handler, ["__init__"])
class OrkesTaskClient(OrkesBaseClient, TaskClient):
    """
    A class to manage Tasks executions in a workflow. It allows management of
    tasks including polling, updating task status and adding task logs.
    """

    def poll_task(
        self,
        task_type: str,
        worker_id: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> Optional[Task]:
        kwargs = {}
        if worker_id:
            kwargs.update({"workerid": worker_id})
        if domain:
            kwargs.update({"domain": domain})

        return self.task_resource_api.poll(task_type, **kwargs)

    def batch_poll_tasks(
        self,
        task_type: str,
        worker_id: Optional[str] = None,
        count: Optional[int] = None,
        timeout_in_millisecond: Optional[int] = None,
        domain: Optional[str] = None,
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

        return self.task_resource_api.batch_poll(task_type, **kwargs)

    def get_task(self, task_id: str) -> Task:
        return self.task_resource_api.get_task(task_id)

    def update_task(self, task_result: TaskResult) -> str:
        return self.task_resource_api.update_task(task_result)

    def update_task_by_ref_name(
        self,
        workflow_id: str,
        task_ref_name: str,
        status: str,
        output: object,
        worker_id: Optional[str] = None,
    ) -> str:
        body = {"result": output}
        kwargs = {}
        if worker_id:
            kwargs.update({"workerid": worker_id})
        return self.task_resource_api.update_task1(
            body, workflow_id, task_ref_name, status, **kwargs
        )

    def update_task_sync(
        self,
        workflow_id: str,
        task_ref_name: str,
        status: str,
        output: object,
        worker_id: Optional[str] = None,
    ) -> Workflow:
        body = {"result": output}
        kwargs = {}
        if worker_id:
            kwargs.update({"workerid": worker_id})
        return self.task_resource_api.update_task_sync(
            body, workflow_id, task_ref_name, status, **kwargs
        )

    def get_queue_size_for_task(self, task_type: str) -> int:
        queue_sizes_by_task_type = self.task_resource_api.size(task_type=[task_type])
        queue_size = queue_sizes_by_task_type.get(task_type, 0)
        return queue_size

    def add_task_log(self, task_id: str, log_message: str):
        self.task_resource_api.log(log_message, task_id)

    def get_task_logs(self, task_id: str) -> List[TaskExecLog]:
        return self.task_resource_api.get_task_logs(task_id)
