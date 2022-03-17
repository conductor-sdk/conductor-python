from conductor.client.automator.task_handler import TaskHandler
from conductor.client.example.worker.cpp.simple_cpp_worker import SimpleCppWorker
from conductor.client.example.worker.python.simple_python_worker import SimplePythonWorker


def main():
    workers = [
        SimpleCppWorker('cpp_task_example'),
        SimplePythonWorker('python_task_example')
    ]
    with TaskHandler(workers) as task_handler:
        task_handler.start_processes()
        task_handler.join_processes()


if __name__ == '__main__':
    main()
