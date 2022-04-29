from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface


class SimplePythonWorker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('key1', 'value')
        task_result.add_output_data('key2', 42)
        task_result.add_output_data('key3', False)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        return 5


class WorkerA(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('key', 'A')
        task_result.status = TaskResultStatus.COMPLETED
        return task_result


class WorkerB(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('key', 'B')
        task_result.status = TaskResultStatus.COMPLETED
        return task_result


def main():
    # Point to the Conductor Server
    configuration = Configuration(
        base_url='https://play.orkes.io',
        debug=True,
        authentication_settings=AuthenticationSettings(  # Optional if you are using a server that requires authentication
            key_id='key',
            key_secret='secret'
        )
    )

    # Add three workers
    workers = [
        SimplePythonWorker('python_task_example'),
        WorkerA('task_a'),
        WorkerB('task_random_name'),
    ]

    # Start the worker processes and wait for their completion
    with TaskHandler(workers, configuration) as task_handler:
        task_handler.start_processes()
        task_handler.join_processes()


if __name__ == '__main__':
    main()
