from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
import abc
import socket
from typing import Union, List


class WorkerInterface(abc.ABC):
    def __init__(self, task_definition_names: Union[str, list]):
        self.task_definition_names = task_definition_names
        self.next_task_index = 0

    @abc.abstractmethod
    def execute(self, task: Task) -> TaskResult:
        """
        Executes a task and returns the updated task.

        :param Task: (required)
        :return: TaskResult
                 If the task is not completed yet, return with the status as IN_PROGRESS.
        """
        pass

    def get_identity(self) -> str:
        """
        Retrieve the hostname of the instance that the worker is running.

        :return: str
        """
        return socket.gethostname()

    def get_polling_interval_in_seconds(self) -> float:
        """
        Retrieve interval in seconds at which the server should be polled for worker tasks.

        :return: float
                 Default: 100ms
        """
        return 0.1

    def get_task_definition_name(self) -> str:
        """
        Retrieve the name of the task definition the worker is currently working on.

        :return: TaskResult
        """
        if isinstance(self.task_definition_names, list):
            if self.next_task_index >= len(self.task_definition_names):
                self.next_task_index = 0
            task_definition_name = self.task_definition_names[self.next_task_index]
            if self.next_task_index == (len(self.task_definition_names) - 1):
                self.next_task_index = 0
            else:
                self.next_task_index += 1
            return task_definition_name
        return self.task_definition_names

    def get_task_result_from_task(self, task: Task) -> TaskResult:
        """
        Retrieve the TaskResult object from given task.

        :param Task: (required)
        :return: TaskResult
        """
        return TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id=self.get_identity()
        )

    def get_domain(self) -> str:
        """
        Retrieve the domain of the worker.

        :return: str
        """
        return None

    def paused(self) -> bool:
        """
        Override this method to pause the worker from polling.
        """
        return False
