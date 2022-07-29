from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface
from typing import Any


class FaultyExecutionWorker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        raise Exception('faulty execution')


class SimplePythonWorker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('worker_style', 'class')
        task_result.add_output_data('secret_number', 1234)
        task_result.add_output_data('is_it_true', False)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        # poll every 500ms
        return 0.5


def worker_with_task_result(task: Task) -> TaskResult:
    task_result = TaskResult(
        task_id=task.task_id,
        workflow_instance_id=task.workflow_instance_id,
        worker_id='your_custom_id'
    )
    task_result.add_output_data('worker_style', 'function')
    task_result.add_output_data('worker_input', 'Task')
    task_result.add_output_data('worker_output', 'TaskResult')
    task_result.status = TaskResultStatus.COMPLETED
    return task_result


def worker_with_generic_return(task: Task) -> Any:
    return {
        'worker_style': 'function',
        'worker_input': 'Task',
        'worker_output': 'Any'
    }
