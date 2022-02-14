from conductor.client.automator.task_runner import TaskRunner
import logging
import multiprocessing
import os

logger = logging.getLogger(
    '.'.join(
        [
            str(os.getpid()),
            __name__
        ]
    )
)


class TaskHandler:
    def __init__(self, configuration, workers):
        self.task_runner_processes = []
        for worker in workers:
            task_runner = TaskRunner(configuration, worker)
            process = multiprocessing.Process(
                target=task_runner.run
            )
            self.task_runner_processes.append(process)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for task_runner_process in self.task_runner_processes:
            try:
                task_runner_process.kill()
            except:
                task_runner_process.terminate()

    def start(self):
        for task_runner_process in self.task_runner_processes:
            task_runner_process.start()
        logger.info('Started all TaskRunner processes')
        for task_runner_process in self.task_runner_processes:
            task_runner_process.join()
        logger.info('Joined all TaskRunner processes')
