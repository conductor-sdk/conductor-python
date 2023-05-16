from typing import Callable, TypeVar
from conductor.client.worker.worker import ExecuteTaskFunction


class WorkerTask(ExecuteTaskFunction):
    def __init__(self, task_type: str, domain: str = None, poll_interval_seconds: float = None, workerid: str = None):
        self.task_type = task_type
        self.domain = domain
        self.poll_interval = poll_interval_seconds
        self.workerid = workerid
