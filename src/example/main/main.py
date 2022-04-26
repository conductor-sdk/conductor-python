from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.settings.authentication_settings import AuthenticationSettings
from conductor.client.settings.external_storage_settings import ExternalStorageSettings
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


def upload_task_result_payload_and_get_path(task_result: TaskResult) -> str:
    # TODO add some real implementation
    return 'REMOTE_PATH'


def main():
    # Point to the Conductor Server
    configuration = Configuration(
        base_url='https://play.orkes.io',
        debug=True,
        authentication_settings=AuthenticationSettings(  # Optional if you are using a server that requires authentication
            key_id='id',
            key_secret='secret'
        ),
        external_storage_settings=ExternalStorageSettings(  # Optional if you are using an external storage server
            external_storage_handler=upload_task_result_payload_and_get_path,
        )
    )

    # Add three workers
    workers = [
        SimplePythonWorker('python_task_example'),
        WorkerA('task_A'),
        WorkerB('task_B'),
    ]

    # Start the worker processes and wait for their completion
    with TaskHandler(workers, configuration) as task_handler:
        task_handler.start_processes()
        task_handler.join_processes()


if __name__ == '__main__':
    main()
