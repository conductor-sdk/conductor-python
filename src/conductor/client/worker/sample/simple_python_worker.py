from conductor.client.http.models.task_result import TaskResult
from conductor.client.worker.worker_interface import WorkerInterface


class SimplePythonWorker(WorkerInterface):
    def __init__(self):
        super().__init__('simple_python_worker')

    def execute(self, task):
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id=self.get_task_definition_name()
        )
        self.__execute(task_result)
        task_result.status = 'COMPLETED'
        return task_result

    def __execute(self, task_result):
        task_result.add_output_data('key', 'value')
