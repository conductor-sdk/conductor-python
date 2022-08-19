from conductor.client.automator.task_runner import run
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.worker.worker_interface import WorkerInterface
from typing import List
import logging
import threading

_logger = logging.getLogger(__name__)


class TaskHandler:
    def __init__(
            self,
            workers: List[WorkerInterface],
            configuration: Configuration = None,
            metrics_settings: MetricsSettings = None,
    ):
        self.configuration = configuration
        self.metrics_configuration = metrics_settings

        self._task_resource_api = TaskResourceApi(
            ApiClient(
                configuration
            )
        )

        self._running_workers = {}
        self._running_workers_mutex = threading.Lock()

        if not isinstance(workers, list):
            workers = [workers]
        self.start_worker(*workers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_processes()

    def stop_processes(self) -> None:
        _logger.info('Stopped all processes')

    def start_processes(self) -> None:
        _logger.info('Started all processes')

    def join_processes(self) -> None:
        _logger.info('Joined all processes')

    def start_worker(self, *workers: WorkerInterface) -> None:
        for worker in workers:
            self.__start_worker(worker)
        _logger.info(f'Started {len(workers)} workers')

    def __start_worker(self, worker: WorkerInterface) -> None:
        if not isinstance(worker, WorkerInterface):
            _logger.warning(
                'Failed to start worker, object must be of WorkerInterface type'
            )
            return
        with self._running_workers_mutex:
            if worker.task_definition_name in self._running_workers:
                _logger.warning(
                    f'Worker already started for {worker.task_definition_name}, you must stop a worker before attempting to start it again'
                )
                return
            worker_thread = self.__generate_worker_thread(worker)
            self._running_workers[worker.task_definition_name] = worker_thread

    def __generate_worker_thread(self, worker: WorkerInterface) -> threading.Thread:
        return threading.Thread(
            target=run,
            args=(
                self.configuration,
                worker.get_task_definition_name(),
                worker.get_polling_interval_in_seconds(),
                worker.execute,
                worker.get_identity(),
                worker.get_domain(),
                None,
            )
        )
