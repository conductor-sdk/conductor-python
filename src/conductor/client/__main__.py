from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.worker.sample.python.faulty_execution_worker import FaultyExecutionWorker
from conductor.client.worker.sample.python.simple_python_worker import SimplePythonWorker


def main():
    configuration = Configuration(
        base_url='https://play.orkes.io',
        debug=True,
        authentication_settings=AuthenticationSettings(
            key_id='id',
            key_secret='secret'
        )
    )
    task_definition_name = 'python_task_example'
    workers = [
        FaultyExecutionWorker(task_definition_name),
        SimplePythonWorker(task_definition_name)
    ]
    with TaskHandler(workers, configuration) as task_handler:
        task_handler.start_processes()
        task_handler.join_processes()


if __name__ == '__main__':
    main()
