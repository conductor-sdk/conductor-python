from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from typing_extensions import Self
import abc
import socket


class WorkerInterface(abc.ABC):
    def __init__(self, task_definition_name: str, batch_size: int = None) -> Self:
        self.task_definition_name = task_definition_name
        self.batch_size = batch_size

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
        return self.task_definition_name

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

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int) -> None:
        if batch_size == None:
            batch_size = 1
        if not isinstance(batch_size, int):
            raise Exception('Batch size must be of integer type')
        if batch_size < 1:
            raise Exception('Batch size must be have a positive value')
        self._batch_size = batch_size

    @property
    def task_definition_name(self) -> str:
        return self._task_definition_name

    @task_definition_name.setter
    def task_definition_name(self, task_definition_name: str) -> None:
        if not isinstance(task_definition_name, str):
            raise Exception('Task definition name must be of string type')
        if task_definition_name is None or task_definition_name == '':
            raise Exception('Task definition name must not be empty')
        self._task_definition_name = task_definition_name
