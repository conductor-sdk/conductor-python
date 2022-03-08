from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from conductor.client.telemetry.metrics_collector import MetricsCollector
from conductor.client.worker.worker_interface import WorkerInterface
from multiprocessing import Process
from typing import List
import logging

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


class TaskHandler:
    def __init__(
            self,
            workers: List[WorkerInterface],
            configuration: Configuration = None
    ):
        if not isinstance(workers, list):
            raise Exception('Invalid worker list')
        self.__create_metrics_provider_process()
        self.__create_task_runner_processes(workers, configuration)
        logger.info('Created all processes')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__stop_metrics_provider_process()
        self.__stop_task_runner_processes()

    def start_processes(self) -> None:
        self.__start_metrics_provider_process()
        self.__start_task_runner_processes()
        logger.info('Started all processes')

    def join_processes(self) -> None:
        self.__join_metrics_provider_process()
        self.__join_task_runner_processes()
        logger.info('Joined all processes')

    def __create_metrics_provider_process(self):
        self.metrics_provider_process = Process(
            target=MetricsCollector.provide_metrics
        )
        logger.info('Created MetricsProvider process')

    def __create_task_runner_processes(self, workers, configuration):
        self.task_runner_processes = []
        for worker in workers:
            self.__create_task_runner_process(worker, configuration)
        logger.info('Created TaskRunner processes')

    def __create_task_runner_process(self, worker, configuration):
        task_runner = TaskRunner(worker, configuration)
        process = Process(
            target=task_runner.run
        )
        self.task_runner_processes.append(process)

    def __start_metrics_provider_process(self):
        self.metrics_provider_process.start()
        logger.info('Started MetricsProvider process')

    def __start_task_runner_processes(self):
        for task_runner_process in self.task_runner_processes:
            task_runner_process.start()
        logger.info('Started TaskRunner processes')

    def __join_metrics_provider_process(self):
        self.metrics_provider_process.join()
        logger.info('Joined MetricsProvider processes')

    def __join_task_runner_processes(self):
        for task_runner_process in self.task_runner_processes:
            task_runner_process.join()
        logger.info('Joined TaskRunner processes')

    def __stop_metrics_provider_process(self):
        self.__stop_process(self.metrics_provider_process)

    def __stop_task_runner_processes(self):
        for task_runner_process in self.task_runner_processes:
            self.__stop_process(task_runner_process)

    def __stop_process(self, process: Process):
        if process == None:
            return
        try:
            process.kill()
            logger.info(f'Killed process: {process}')
        except Exception as e:
            logger.debug(f'Failed to kill process: {process}, reason: {e}')
            self.metrics_provider_process.terminate()
            logger.info('Terminated process: {process}')
