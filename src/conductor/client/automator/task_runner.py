from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.telemetry.metrics_collector import MetricsCollector
from copy import deepcopy
from typing import Callable
import logging
import multiprocessing
import sys
import threading
import time
import traceback

_logger = logging.get_logger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)

_TASK_UPDATE_RETRY_ATTEMPTS_LIMIT = 3
_BATCH_POLL_ERROR_RETRY_INTERVAL = 0.1  # 100ms
_BATCH_POLL_NO_AVAILABLE_WORKER_RETRY_INTERVAL = 0.001  # 1ms


def _batch_poll(
    task_resource_api: TaskResourceApi,
    task_name: str,
    batch_size: int,
    timeout: str,
    worker_id: str = None,
    domain: str = None,
    metrics_collector: MetricsCollector = None,
) -> Task:
    if batch_size < 1:
        return None
    _logger.debug(
        f'Polling for the next {batch_size} task(s) with name {task_name}'
    )
    kwargs = {
        'count': batch_size,
        'timeout': timeout,
    }
    if domain is not None:
        kwargs['domain'] = domain
    if worker_id is not None:
        kwargs['workerid'] = worker_id
    try:
        start_time = time.time()
        tasks = task_resource_api.batch_poll(
            tasktype=task_name,
            **kwargs,
        )
        time_spent = time.time() - start_time
    except Exception as e:
        if metrics_collector is not None:
            metrics_collector.increment_task_poll_error(
                task_name, type(e)
            )
        _logger.info(
            f'Failed to poll task for: {task_name}, reason: {traceback.format_exc()}'
        )
        return None
    if metrics_collector is not None:
        metrics_collector.increment_task_poll(
            task_name
        )
        metrics_collector.record_task_poll_time(
            task_name, time_spent
        )
    if tasks != None:
        _logger.debug(
            'Polled {} task(s) of type {} with worker_id {} and domain {}'.format(
                len(tasks), task_name, worker_id, domain
            )
        )
    return tasks


def _worker_process_daemon(
    task_resource_api: TaskResourceApi,
    task: Task,
    worker_execution_function: Callable[[Task], TaskResult],
    worker_id: str = None,
    metrics_collector: MetricsCollector = None,
):
    # apply_logging_config()
    task_result = _execute_task(
        task,
        worker_execution_function,
        worker_id,
        metrics_collector
    )
    _update_task(
        task.task_def_name,
        task_result,
        task_resource_api,
        metrics_collector
    )


def _execute_task(
    task: Task,
    worker_execution_function: Callable[[Task], TaskResult],
    worker_id: str = None,
    metrics_collector: MetricsCollector = None,
) -> TaskResult:
    task_name = task.task_def_name
    _logger.debug(
        'Executing task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}'.format(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            task_definition_name=task_name
        )
    )
    try:
        start_time = time.time()
        task_result = worker_execution_function(task)
        time_spent = time.time() - start_time
    except Exception as e:
        if metrics_collector is not None:
            metrics_collector.increment_task_execution_error(
                task_name, type(e)
            )
        failed_task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id=worker_id
        )
        failed_task_result.status = TaskResultStatus.FAILED
        failed_task_result.reason_for_incompletion = str(e)
        _logger.info(
            'Failed to execute task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}, reason: {reason}'.format(
                task_id=task.task_id,
                workflow_instance_id=task.workflow_instance_id,
                task_definition_name=task_result,
                reason=traceback.format_exc()
            )
        )
        return failed_task_result
    if metrics_collector is not None:
        metrics_collector.record_task_execute_time(
            task_name,
            time_spent
        )
    _logger.debug(
        'Executed task, id: {}, workflow_instance_id: {}, task_definition_name: {}'.format(
            task.task_id, task.workflow_instance_id, task_name
        )
    )
    return task_result


def _update_task(
    task_name: str,
    task_result: TaskResult,
    task_resource_api: TaskResourceApi,
    metrics_collector: MetricsCollector = None,
) -> None:
    _logger.debug(
        'Updating task, id: {}, workflow_instance_id: {}, task_definition_name: {}'.format(
            task_id=task_result.task_id,
            workflow_instance_id=task_result.workflow_instance_id,
            task_definition_name=task_name
        )
    )
    for attempt in range(_TASK_UPDATE_RETRY_ATTEMPTS_LIMIT + 1):
        if attempt > 0:
            # sleeps for [10s, 20s, 30s] on failure
            time.sleep(attempt * 10)
        try:
            start_time = time.time()
            response = task_resource_api.update_task(
                body=task_result
            )
            time_spent = time.time() - start_time
            break
        except Exception as e:
            if metrics_collector is not None:
                metrics_collector.increment_task_update_error(
                    task_name, type(e)
                )
            _logger.debug(
                'Failed to update task, id: {}, workflow_instance_id: {}, task_definition_name: {}, reason: {}'.format(
                    task_result.task_id,
                    task_result.workflow_instance_id,
                    task_name,
                    traceback.format_exc()
                )
            )
    if metrics_collector is not None:
        metrics_collector.record_task_result_payload_size(
            task_name,
            sys.getsizeof(task_result)
        )
        metrics_collector.record_task_update_time(
            task_name,
            time_spent
        )
    _logger.debug(
        'Updated task, id: {}, workflow_instance_id: {}, task_definition_name: {}, response: {}'.format(
            task_result.task_id,
            task_result.workflow_instance_id,
            task_name,
            response
        )
    )
    return response


class TaskRunner:
    def __init__(
        self,
        configuration: Configuration,
        task_definition_name: str,
        batch_size: int,
        polling_interval: float,
        worker_execution_function: Callable[[Task], TaskResult],
        worker_id: str = None,
        domain: str = None,
        metrics_settings: MetricsSettings = None
    ):
        self.configuration = configuration
        self._task_resource_api = TaskResourceApi(
            ApiClient(configuration)
        )

        self._task_name = task_definition_name

        self._batch_size_mutex = threading.Lock()
        self.batch_size = batch_size

        self._poll_interval_mutex = threading.Lock()
        self.poll_interval = polling_interval

        self._worker_execution_function_mutex = threading.Lock()
        self.worker_execution_function = worker_execution_function

        self._worker_id_mutex = threading.Lock()
        self.worker_id = worker_id

        self._domain_mutex = threading.Lock()
        self.domain = domain

        self._running_workers_mutex = threading.Lock()
        self._running_workers = {}  # {key=pid, value=process}

        self._paused_worker_mutex = threading.Lock()
        self._paused_worker = False

        self.metrics_collector = None
        if metrics_settings is not None:
            self.metrics_collector = MetricsCollector(
                metrics_settings
            )

    def __start_worker(self, task: Task) -> None:
        worker_process = multiprocessing.Process(
            target=_worker_process_daemon,
            args=(
                self._task_resource_api,
                task,
                self.worker_execution_function,
                self.worker_id,
                self.metrics_collector
            )
        )
        with self._running_workers_mutex:
            self._running_workers[worker_process.pid] = worker_process
        worker_process.start()
        _logger.debug(
            'Started worker for task {} with task_id {} - pid: {}'.format(
                self._task_name,
                task.task_id,
                worker_process.pid
            )
        )
        worker_monitor_thread = threading.Thread(
            target=self.__monitor_running_worker,
            args=(
                worker_process,
                task.task_id,
            )
        )
        worker_monitor_thread.start()

    def __monitor_running_worker(self, worker_process: multiprocessing.Process, task_id: str) -> None:
        worker_process.join()
        with self._running_workers_mutex:
            del self._running_workers[worker_process.pid]
        _logger.debug(
            'Finished worker for task {} with task_id {} - pid: {}'.format(
                self._task_name,
                task_id,
                worker_process.pid
            )
        )

    def run(self) -> None:
        while True:
            try:
                self.run_once()
            except Exception as e:
                if self.metrics_collector is not None:
                    self.metrics_collector.increment_uncaught_exception()
                _logger.debug(
                    f'Exception raised while running worker for task: {self._task_name}. Reason: {str(e)}'
                )

    def run_once(self) -> None:
        if self.is_worker_paused():
            time.sleep(_BATCH_POLL_ERROR_RETRY_INTERVAL)
            return
        available_workers = self.batch_size - self.running_workers
        if available_workers < 1:
            time.sleep(_BATCH_POLL_NO_AVAILABLE_WORKER_RETRY_INTERVAL)
            return
        tasks = _batch_poll(
            task_resource_api=self._task_resource_api,
            task_name=self._task_name,
            batch_size=available_workers,
            poll_interval=self.poll_interval,
            worker_id=self.worker_id,
            domain=self.domain,
        )
        for task in tasks:
            self.__start_worker(task)
        time.sleep(self.poll_interval)

    @property
    def batch_size(self) -> int:
        with self._batch_size_mutex:
            return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int) -> None:
        with self._batch_size_mutex:
            self._batch_size = deepcopy(batch_size)

    @property
    def poll_interval(self) -> float:
        with self._poll_interval_mutex:
            return self._poll_interval

    @poll_interval.setter
    def poll_interval(self, poll_interval: float) -> None:
        with self._poll_interval_mutex:
            self._poll_interval = deepcopy(poll_interval)

    @property
    def worker_execution_function(self) -> Callable[[Task], TaskResult]:
        with self._worker_id_mutex:
            return self._worker_id

    @worker_execution_function.setter
    def worker_execution_function(self, worker_execution_function: Callable[[Task], TaskResult]) -> None:
        with self._worker_execution_function_mutex:
            self._worker_execution_function = deepcopy(
                worker_execution_function)

    @property
    def worker_id(self) -> str:
        with self._worker_id_mutex:
            return self._worker_id

    @worker_id.setter
    def worker_id(self, worker_id: str) -> None:
        with self._worker_id_mutex:
            self._worker_id = deepcopy(worker_id)

    @property
    def domain(self) -> str:
        with self._domain_mutex:
            return self._domain

    @domain.setter
    def domain(self, domain: str) -> None:
        with self._domain_mutex:
            self._domain = deepcopy(domain)

    @property
    def running_workers(self) -> int:
        with self._running_workers_mutex:
            return len(self._running_workers)

    def resume_worker(self) -> None:
        with self._paused_worker_mutex:
            self._paused_worker = False

    def pause_worker(self) -> None:
        with self._paused_worker_mutex:
            self._paused_worker = True

    def is_worker_paused(self) -> bool:
        with self._paused_worker_mutex:
            return self._paused_worker
