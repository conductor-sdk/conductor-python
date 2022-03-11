from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.sample.faulty_execution_worker import FaultyExecutionWorker
from conductor.client.worker.sample.simple_python_worker import SimplePythonWorker


def main():
    configuration = Configuration(debug=True)
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
