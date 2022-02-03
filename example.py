from src.worker.simple_python_worker import SimplePythonWorker
from src.automator.parallel_task_handler import ParallelTaskHandler
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    workers = [SimplePythonWorker()] * 8
    task_runner = ParallelTaskHandler(workers)
    task_runner.start()


if __name__ == '__main__':
    main()
