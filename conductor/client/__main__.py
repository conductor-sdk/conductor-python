from conductor.client.automator.task_handler import TaskHandler
from conductor.client.worker.simple_python_worker import SimplePythonWorker


def main():
    workers = [SimplePythonWorker()] * 1
    with TaskHandler(workers) as parallel_task_handler:
        parallel_task_handler.start()


if __name__ == '__main__':
    main()
