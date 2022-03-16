from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface


class TaskWorker(WorkerInterface):
    def __init__(self, name, execute_function):
        self.execute_function = execute_function
        self.task_definition_name = name

    def execute(self, task: Task) -> TaskResult:
        result = self.execute_function(task)

        if isinstance(result, TaskResult):
            task_result = result
            task_result.task_id = task.task_id
            task_result.workflow_instance_id = task.workflow_instance_id,
            task_result.worker_id = self.get_identity()
        else:
            task_result = self.get_task_result_from_task(task)
            if isinstance(result, dict):
                task_result.output_data = result
            else:
                task_result.output_data = str(result)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result