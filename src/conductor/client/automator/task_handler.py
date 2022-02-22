from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.worker_interface import WorkerInterface
from typing import List
import logging
import multiprocessing

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


class TaskHandler:
    def __init__(self, workers: List[WorkerInterface], configuration: Configuration = None):
        if not isinstance(workers, list):
            raise Exception('Invalid worker list')
        self.task_runner_processes = []
        for worker in workers:
            task_runner = TaskRunner(worker, configuration)
            process = multiprocessing.Process(
                target=task_runner.run
            )
            self.task_runner_processes.append(process)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def start(self) -> None:
        for task_runner_process in self.task_runner_processes:
            task_runner_process.start()
        logger.info('Started all TaskRunner processes')
        for task_runner_process in self.task_runner_processes:
            task_runner_process.join()
        logger.info('Joined all TaskRunner processes')
