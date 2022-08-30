from calendar import c
from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.telemetry.metrics_collector import MetricsCollector
from conductor.client.worker.worker_interface import WorkerInterface
from multiprocessing import Process
from typing import List
from typing_extensions import Self
import logging
import threading

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


class TaskHandler:
    def __init__(
        self,
        workers: List[WorkerInterface],
        configuration: Configuration = None,
        metrics_settings: MetricsSettings = None
    ) -> Self:
        if not isinstance(workers, list):
            workers = [workers]
        self.configuration = configuration
        self.metrics_settings = metrics_settings

        self._task_runner = {}
        self._task_runner_thread = {}
        self._task_runner_mutex = threading.Lock()

        self.start_worker(*workers)
        self.__create_metrics_provider_process()
        logger.info('Created all processes')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_processes()

    def stop_processes(self) -> None:
        self.__stop_metrics_provider_process()

    def start_processes(self) -> None:
        self.__start_metrics_provider_process()
        logger.info('Started all processes')

    def join_processes(self) -> None:
        self.__join_workers()
        self.__join_metrics_provider_process()
        logger.info('Joined all processes')

    def __create_metrics_provider_process(self) -> None:
        if self.metrics_settings == None:
            self.metrics_provider_process = None
            return
        self.metrics_provider_process = Process(
            target=MetricsCollector.provide_metrics,
            args=(self.metrics_settings,)
        )
        logger.info('Created MetricsProvider process')

    def start_worker(self, *workers: WorkerInterface) -> None:
        for worker in workers:
            self.__start_worker(worker)
        logger.info('Created TaskRunner processes')

    def __start_worker(self, worker: WorkerInterface):
        task_name = worker.get_task_definition_name()
        with self._task_runner_mutex:
            if task_name in self._task_runner:
                raise Exception(f'worker already started for {task_name}')
            task_runner = TaskRunner(
                configuration=self.configuration,
                task_definition_name=worker.task_definition_name,
                batch_size=worker.batch_size,
                polling_interval=worker.polling_interval,
                worker_execution_function=worker.execute,
                worker_id=worker.get_identity(),
                domain=worker.get_domain(),
                metrics_settings=self.metrics_settings
            )
            self._task_runner[task_name] = task_runner
            task_runner_thread = threading.Thread(target=task_runner.run)
            self._task_runner_thread[task_name] = task_runner_thread
            task_runner_thread.start()

    def __start_metrics_provider_process(self):
        if self.metrics_provider_process == None:
            return
        self.metrics_provider_process.start()
        logger.info('Started MetricsProvider process')

    def __join_metrics_provider_process(self):
        if self.metrics_provider_process == None:
            return
        self.metrics_provider_process.join()
        logger.info('Joined MetricsProvider processes')

    def __join_workers(self):
        with self._task_runner_mutex:
            for thread in self._task_runner_thread:
                thread.join()
        logger.info('Joined all workers')

    def __stop_metrics_provider_process(self):
        self.__stop_process(self.metrics_provider_process)

    def __stop_process(self, process: Process):
        if process == None:
            return
        try:
            process.kill()
            logger.info(f'Killed process: {process}')
        except Exception as e:
            logger.debug(f'Failed to kill process: {process}, reason: {e}')
            process.terminate()
            logger.info('Terminated process: {process}')
