from src.automator.task_runner import TaskRunner
from src.worker.simple_python_worker import SimplePythonWorker
from src.configuration import Configuration


def main():
    configuration = Configuration()
    worker = SimplePythonWorker()
    task_runner = TaskRunner(worker)
    task_runner.start()


if __name__ == '__main__':
    main()
