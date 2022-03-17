from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface


class TaskWorker(WorkerInterface):
    def __init__(self, name, execute_function):
        super().__init__(name)
        self.execute_function = execute_function

    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        execution_return_value = self.execute_function(task)
        if not isinstance(execution_return_value, dict):
            execution_return_value = {execution_return_value}
        task_result = execution_return_value
        task_result.status = TaskResultStatus.COMPLETED
        return task_result
