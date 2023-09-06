from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_exec_log import TaskExecLog
from conductor.client.telemetry.metrics_collector import MetricsCollector
from conductor.client.worker.worker_interface import WorkerInterface
import logging
import sys
import time
import traceback

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


class TaskRunner:
    def __init__(
        self,
        worker: WorkerInterface,
        configuration: Configuration = None,
        metrics_settings: MetricsSettings = None
    ):
        if not isinstance(worker, WorkerInterface):
            raise Exception('Invalid worker')
        self.worker = worker
        if not isinstance(configuration, Configuration):
            configuration = Configuration()
        self.configuration = configuration
        self.metrics_collector = None
        if metrics_settings is not None:
            self.metrics_collector = MetricsCollector(
                metrics_settings
            )
        self.task_client = TaskResourceApi(
            ApiClient(
                configuration=self.configuration
            )
        )

    def run(self) -> None:
        if self.configuration != None:
            self.configuration.apply_logging_config()
        while True:
            try:
                self.run_once()
            except Exception:
                pass

    def run_once(self) -> None:
        task = self.__poll_task()
        if task != None and task.task_id != None:
            task_result = self.__execute_task(task)
            self.__update_task(task_result)
        self.__wait_for_polling_interval()

    def __poll_task(self) -> Task:
        task_definition_name = self.worker.get_task_definition_name()
        if self.worker.paused():
            logger.warning(f'Stop polling task for: {task_definition_name}')
            return None
        if self.metrics_collector is not None:
            self.metrics_collector.increment_task_poll(
                task_definition_name
            )
        logger.debug(f'Polling task for: {task_definition_name}')
        try:
            start_time = time.time()
            domain = self.worker.get_domain()
            params = {'workerid': self.worker.get_identity()}
            if domain != None:
                params['domain'] = domain
            task = self.task_client.poll(
                tasktype=task_definition_name,
                **params
            )
            finish_time = time.time()
            time_spent = finish_time - start_time
            if self.metrics_collector is not None:
                self.metrics_collector.record_task_poll_time(
                    task_definition_name, time_spent
                )
        except Exception as e:
            if self.metrics_collector is not None:
                self.metrics_collector.increment_task_poll_error(
                    task_definition_name, type(e)
                )
            logger.error(
                f'Failed to poll task for: {task_definition_name}, reason: {traceback.format_exc()}'
            )
            return None
        if task != None:
            logger.debug(
                f'Polled task: {task_definition_name}, worker_id: {self.worker.get_identity()}'
            )
        return task

    def __execute_task(self, task: Task) -> TaskResult:
        if not isinstance(task, Task):
            return None
        task_definition_name = self.worker.get_task_definition_name()
        logger.debug(
            'Executing task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}'.format(
                task_id=task.task_id,
                workflow_instance_id=task.workflow_instance_id,
                task_definition_name=task_definition_name
            )
        )
        try:
            start_time = time.time()
            task_result = self.worker.execute(task)
            finish_time = time.time()
            time_spent = finish_time - start_time
            if self.metrics_collector is not None:
                self.metrics_collector.record_task_execute_time(
                    task_definition_name,
                    time_spent
                )
                self.metrics_collector.record_task_result_payload_size(
                    task_definition_name,
                    sys.getsizeof(task_result)
                )
            logger.debug(
                'Executed task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}'.format(
                    task_id=task.task_id,
                    workflow_instance_id=task.workflow_instance_id,
                    task_definition_name=task_definition_name
                )
            )
        except Exception as e:
            if self.metrics_collector is not None:
                self.metrics_collector.increment_task_execution_error(
                    task_definition_name, type(e)
                )
            task_result = TaskResult(
                task_id=task.task_id,
                workflow_instance_id=task.workflow_instance_id,
                worker_id=self.worker.get_identity()
            )
            task_result.status = 'FAILED'
            task_result.reason_for_incompletion = str(e)
            task_result.logs = [TaskExecLog(
                traceback.format_exc(), task_result.task_id, int(time.time()))]
            logger.error(
                'Failed to execute task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}, reason: {reason}'.format(
                    task_id=task.task_id,
                    workflow_instance_id=task.workflow_instance_id,
                    task_definition_name=task_definition_name,
                    reason=traceback.format_exc()
                )
            )
        return task_result

    def __update_task(self, task_result: TaskResult):
        if not isinstance(task_result, TaskResult):
            return None
        task_definition_name = self.worker.get_task_definition_name()
        logger.debug(
            'Updating task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}'.format(
                task_id=task_result.task_id,
                workflow_instance_id=task_result.workflow_instance_id,
                task_definition_name=task_definition_name
            )
        )
        for attempt in range(4):
            if attempt > 0:
                # Wait for [10s, 20s, 30s] before next attempt
                time.sleep(attempt * 10)
            try:
                response = self.task_client.update_task(body=task_result)
                logger.debug(
                    'Updated task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}, response: {response}'.format(
                        task_id=task_result.task_id,
                        workflow_instance_id=task_result.workflow_instance_id,
                        task_definition_name=task_definition_name,
                        response=response
                    )
                )
                return response
            except Exception as e:
                if self.metrics_collector is not None:
                    self.metrics_collector.increment_task_update_error(
                        task_definition_name, type(e)
                    )
                logger.error(
                    'Failed to update task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}, reason: {reason}'.format(
                        task_id=task_result.task_id,
                        workflow_instance_id=task_result.workflow_instance_id,
                        task_definition_name=task_definition_name,
                        reason=traceback.format_exc()
                    )
                )
        return None

    def __wait_for_polling_interval(self) -> None:
        polling_interval = self.worker.get_polling_interval_in_seconds()
        logger.debug(f'Sleep for {polling_interval} seconds')
        time.sleep(polling_interval)
