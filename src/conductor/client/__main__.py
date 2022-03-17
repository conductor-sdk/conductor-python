from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.example.worker.cpp.simple_cpp_worker import SimpleCppWorker


def main():
    configuration = Configuration(
        base_url='https://play.orkes.io',
        debug=True,
        authentication_settings=AuthenticationSettings(
            key_id='id',
            key_secret='secret'
        )
    )
    workers = [
        SimpleCppWorker('simple_cpp_task')
    ]
    with TaskHandler(workers, configuration) as task_handler:
        task_handler.start_processes()
        task_handler.join_processes()


if __name__ == '__main__':
    main()
