from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.worker.worker_interface import WorkerInterface


class FaultyExecutionWorker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        raise Exception('faulty execution')
