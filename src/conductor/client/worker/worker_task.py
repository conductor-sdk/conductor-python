from typing import Callable, TypeVar
from conductor.client.worker.worker import ExecuteTaskFunction


class WorkerTask(ExecuteTaskFunction):
    def __init__(self, task_definition_name: str = None,domain: str = None, poll_interval: float = None, worker_id: str = None):
        """
        Task Worker
        Parameters
        ----------
        task_definition_name name of the task to poll for
        domain task domain
        poll_interval polling interval in millisecond
        worker_id (optional) id of the worker.  defaults to hostname if not specified
        """
        self.task_definition_name = task_definition_name
        self.domain = domain
        self.poll_interval = poll_interval
        self.worker_id = worker_id

    def __call__(self, *args, **kwargs):
        pass
