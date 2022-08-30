from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.telemetry.metrics_collector import MetricsCollector
from typing import Callable
import logging
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


class TaskRunner:
    def __init__(
        self,
        configuration: Configuration,
        task_definition_name: str,
        batch_size: int,
        polling_interval: float,
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

        self._running_workers_mutex = threading.Lock()
        self._running_workers = 0

        self._paused_worker = True
        self._paused_worker_mutex = threading.Lock()

        self.metrics_collector = None
        if metrics_settings is not None:
            self.metrics_collector = MetricsCollector(
                metrics_settings
            )

    def __increase_running_workers(self, amount: int) -> None:
        if amount < 1:
            return
        with self._running_workers_mutex:
            self._running_workers += amount
            _logger.debug(
                'Increased running workers for task {} by {}, new total: {}'.format(
                    self._task_name,
                    amount,
                    self._running_workers
                )
            )

    def __running_worker_done(self) -> None:
        with self._running_workers_mutex:
            self._running_workers -= 1
            _logger.debug(
                'Worker done for task {}, new total: {}'.format(
                    self._task_name,
                    self._running_workers
                )
            )

    @property
    def poll_interval(self) -> float:
        with self._poll_interval_mutex:
            return self._poll_interval

    @poll_interval.setter
    def poll_interval(self, poll_interval: float) -> None:
        with self._poll_interval_mutex:
            self._poll_interval = poll_interval

    @property
    def batch_size(self) -> int:
        with self._batch_size_mutex:
            return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int) -> None:
        with self._batch_size_mutex:
            self._batch_size = batch_size

    # def run(self) -> None:
    #     self.configuration.apply_logging_config()
    #     while True:
    #         try:
    #             self.run_once()
    #         except Exception as e:
    #             if self.metrics_collector is not None:
    #                 self.metrics_collector.increment_uncaught_exception()
    #             _logger.warning(
    #                 f'Exception raised while running worker for task: {self._task_name}. Reason: {str(e)}'
    #             )

    # def run_once() -> None:
    #     available_workers = 1
    #     task = _batch_poll_for_task(
    #         task_resource_api,
    #         task_name,
    #         available_workers,
    #         poll_interval,

    #     )
    #     if task != None:
    #         task_result = self.__execute_task(task)
    #         self.__update_task(task_result)
    #     self.__wait_for_polling_interval()


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


def _wait_for_polling_interval(poll) -> None:
    polling_interval = self.worker.get_polling_interval_in_seconds()
    _logger.debug(f'Sleep for {polling_interval} seconds')
    time.sleep(polling_interval)
