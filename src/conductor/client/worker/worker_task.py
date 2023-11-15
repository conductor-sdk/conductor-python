from typing import Callable, TypeVar
from conductor.client.worker.worker import ExecuteTaskFunction


class WorkerTask(ExecuteTaskFunction):
    def __init__(self, task_definition_name: str, domain: str = None, poll_interval: float = None, worker_id: str = None):
        self.task_definition_name = task_definition_name
        self.domain = domain
        self.poll_interval = poll_interval
        self.worker_id = worker_id

    def __call__(self, *args, **kwargs):
        pass
