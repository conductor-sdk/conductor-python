from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.authentication_resource_api import AuthenticationResourceApi
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.telemetry.metrics_collector import MetricsCollector
from conductor.client.worker.worker_interface import WorkerInterface
import logging
import sys
import time
import traceback

from src.conductor.client.http.models.task_result_status import TaskResultStatus
from src.conductor.client.telemetry.model.metric_external_storage_operation import MetricExternalStorageOperation
from src.conductor.client.telemetry.model.metric_external_storage_payload_type import MetricExternalStoragePayloadType

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

        self.metrics_collector = MetricsCollector(metrics_settings)

    def run(self) -> None:
        if self.configuration != None:
            self.configuration.apply_logging_config()
        while True:
            self.run_once()

    def run_once(self) -> None:
        self.__refresh_auth_token()
        task = self.__poll_task()
        if task != None:
            task_result = self.__execute_task(task)
            self.__update_task(task_result)
        self.__wait_for_polling_interval()

    def __poll_task(self) -> Task:
        task_definition_name = self.worker.get_task_definition_name()
        self.metrics_collector.increment_task_poll(
            task_definition_name
        )
        logger.debug(f'Polling task for: {task_definition_name}')
        try:
            start_time = time.time()
            task = self.__get_task_resource_api().poll(
                tasktype=task_definition_name
            )
            finish_time = time.time()
            time_spent = finish_time - start_time
            self.metrics_collector.record_task_poll_time(
                task_definition_name, time_spent
            )
        except Exception as e:
            self.metrics_collector.increment_task_poll_error(
                task_definition_name, type(e)
            )
            logger.info(
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
            self.metrics_collector.record_task_execute_time(
                task_definition_name,
                time_spent
            )
            logger.debug(
                'Executed task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}'.format(
                    task_id=task.task_id,
                    workflow_instance_id=task.workflow_instance_id,
                    task_definition_name=task_definition_name
                )
            )
        except Exception as e:
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
            logger.info(
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
        self.__evaluateTaskResultExternalStorage(
            task_definition_name, task_result)
        try:
            response = self.__get_task_resource_api().update_task(
                body=task_result
            )
        except Exception as e:
            self.metrics_collector.increment_task_update_error(
                task_definition_name, type(e)
            )
            logger.info(
                'Failed to update task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}, reason: {reason}'.format(
                    task_id=task_result.task_id,
                    workflow_instance_id=task_result.workflow_instance_id,
                    task_definition_name=task_definition_name,
                    reason=traceback.format_exc()
                )
            )
            return None
        logger.debug(
            'Updated task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}, response: {response}'.format(
                task_id=task_result.task_id,
                workflow_instance_id=task_result.workflow_instance_id,
                task_definition_name=task_definition_name,
                response=str(response)
            )
        )
        return response

    def __wait_for_polling_interval(self) -> None:
        polling_interval = self.worker.get_polling_interval_in_seconds()
        logger.debug(f'Sleep for {polling_interval} seconds')
        time.sleep(polling_interval)

    def __get_task_resource_api(self) -> TaskResourceApi:
        return TaskResourceApi(
            ApiClient(
                configuration=self.configuration
            )
        )

    def __refresh_auth_token(self) -> None:
        if (self.configuration.token == None
                and self.configuration.authentication_settings != None):
            token = self.__get_new_token()
            self.configuration.update_token(token)

    def __get_new_token(self) -> str:
        try:
            auth_api = AuthenticationResourceApi(
                ApiClient(self.configuration)
            )
        except Exception:
            logger.debug(
                f'Failed to get new token, reason: {traceback.format_exc()}'
            )
            return None
        return auth_api.token

    def __evaluateTaskResultExternalStorage(self, task_definition_name: str, task_result: TaskResult) -> None:
        size = sys.getsizeof(task_result)
        self.metrics_collector.record_task_result_payload_size(
            task_definition_name, size)
        if self.configuration.external_storage_settings == None:
            return
        if self.__is_task_result_size_above_max_threshold(size):
            message = 'The TaskResult payload size: {payload_size} is greater than the permissible {allowed} bytes",'.format(
                payload_size=size,
                allowed=self.configuration.external_storage_settings.task_output_max_payload_threshold_kb
            )
            logger.warn(message)
            task_result.status = TaskResultStatus.FAILED_WITH_TERMINAL_ERROR
            task_result.reason_for_incompletion = message
            task_result.output_data = None
            return
        if self.__must_upload_task_result_to_external_storage(size):
            self.metrics_collector.increment_external_payload_used(
                task_definition_name,
                MetricExternalStorageOperation.WRITE,
                MetricExternalStoragePayloadType.TASK_OUTPUT
            )
            external_storage_path = self.configuration.external_storage_settings.external_storage_handler(
                task_result.output_data
            )
            task_result.external_output_payload_storage_path = external_storage_path
            task_result.output_data = None

    def __is_task_result_size_above_max_threshold(self, size: int) -> bool:
        return size > self.configuration.external_storage_settings.task_output_max_payload_threshold_kb

    def __must_upload_task_result_to_external_storage(self, size: int) -> bool:
        return size > self.configuration.external_storage_settings.task_output_payload_threshold_kb
