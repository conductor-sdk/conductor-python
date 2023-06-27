from typing import Callable, TypeVar
from .worker import ExecuteTaskFunction


class WorkerTask(ExecuteTaskFunction):
    def __init__(self, task_definition_name: str, domain: str = None, poll_interval: float = None, worker_id: str = None):
        pass

    def __call__(self, *args, **kwargs):
        pass
