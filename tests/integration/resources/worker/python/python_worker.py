from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface
from conductor.client.worker.worker_task import WorkerTask


class FaultyExecutionWorker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        raise Exception('faulty execution')


class ClassWorker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('worker_style', 'class')
        task_result.add_output_data('secret_number', 1234)
        task_result.add_output_data('is_it_true', False)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        # poll every 375ms
        return 0.375


class ClassWorkerWithDomain(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('worker_style', 'class')
        task_result.add_output_data('secret_number', 1234)
        task_result.add_output_data('is_it_true', False)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        # poll every 850ms
        return 0.850

    def get_domain(self) -> str:
        return 'simple_python_worker'


@WorkerTask(task_definition_name='test_python_decorated_worker')
def decorated_worker(input) -> object:
    return {'message': 'python is so cool :)'}


def worker_with_task_input_and_task_result_output(task: Task) -> TaskResult:
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


def worker_with_task_input_and_generic_output(task: Task) -> object:
    return {
        'worker_style': 'function',
        'worker_input': 'Task',
        'worker_output': 'object',
        'task_id': task.task_id,
        'task_input': task.input_data,
    }


def worker_with_generic_input_and_task_result_output(obj: object) -> TaskResult:
    task_result = TaskResult(
        task_id='',
        workflow_instance_id='',
        worker_id=''
    )
    task_result.add_output_data('worker_style', 'function')
    task_result.add_output_data('worker_input', 'object')
    task_result.add_output_data('worker_output', 'TaskResult')
    task_result.status = TaskResultStatus.COMPLETED
    return task_result


def worker_with_generic_input_and_generic_output(obj: object) -> object:
    return {
        'worker_style': 'function',
        'worker_input': 'object',
        'worker_output': 'object',
        'input': obj,
    }
