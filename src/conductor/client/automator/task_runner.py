from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_exec_log import TaskExecLog
from conductor.client.telemetry.metrics_collector import MetricsCollector
from conductor.client.worker.worker_interface import WorkerInterface, DEFAULT_POLLING_INTERVAL
from configparser import ConfigParser
from logging.handlers import QueueHandler
from multiprocessing import Queue
import logging
import sys
import time
import traceback
import os

class TaskRunner:
    def __init__(
        self,
        worker: WorkerInterface,
        configuration: Configuration = None,
        metrics_settings: MetricsSettings = None,
        worker_config: ConfigParser =  None
    ):
        if not isinstance(worker, WorkerInterface):
            raise Exception('Invalid worker')
        self.worker = worker
        self.worker_config = worker_config
        self.__set_worker_properties()
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

    def run(self, queue) -> None:
        # Setup shared logger using Queues
        self.logger = logging.getLogger(
            Configuration.get_logging_formatted_name(
                __name__
            )
        )
        # Add a handler that uses the shared queue
        if queue:
            self.logger.addHandler(QueueHandler(queue))
        
        if self.configuration != None:
            self.configuration.apply_logging_config()
        else:
            self.logger.setLevel(logging.DEBUG)
        
        task_names = ','.join(self.worker.task_definition_names)
        self.logger.info(f'Started worker process for task(s): {task_names}')

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
        self.worker.clear_task_definition_name_cache()

    def __poll_task(self) -> Task:
        task_definition_name = self.worker.get_task_definition_name()
        if self.worker.paused():
            self.logger.debug(f'Stop polling task for: {task_definition_name}')
            return None
        if self.metrics_collector is not None:
            self.metrics_collector.increment_task_poll(
                task_definition_name
            )
        self.logger.debug(f'Polling task for: {task_definition_name}')
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
            self.logger.error(
                f'Failed to poll task for: {task_definition_name}, reason: {traceback.format_exc()}'
            )
            return None
        if task != None:
            self.logger.debug(
                f'Polled task: {task_definition_name}, worker_id: {self.worker.get_identity()}, domain: {self.worker.get_domain()}'
            )
        return task

    def __execute_task(self, task: Task) -> TaskResult:
        if not isinstance(task, Task):
            return None
        task_definition_name = self.worker.get_task_definition_name()
        self.logger.debug(
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
            self.logger.debug(
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
            self.logger.error(
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
        self.logger.debug(
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
                self.logger.debug(
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
                self.logger.error(
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
        self.logger.debug(f'Sleep for {polling_interval} seconds')
        time.sleep(polling_interval)

    def __set_worker_properties(self) -> None:
        # If multiple tasks are supplied to the same worker, then only first
        # task will be considered for setting worker properties
        task_type = self.worker.get_task_definition_name()
        
        # Fetch from ENV Variables if present
        domain = self.__get_property_value_from_env("domain", task_type)
        if domain:
            self.worker.domain = domain

        polling_interval = self.__get_property_value_from_env("polling_interval", task_type)
        polling_interval_initialized = False
        if polling_interval:
            try:
                self.worker.poll_interval = float(polling_interval)
                polling_interval_initialized = True
            except Exception as e:
                self.logger.error("Exception in reading polling interval from environment variable: {0}.".format(str(e)))

        # Fetch from Config if present
        if not domain or not polling_interval_initialized:
            config = self.worker_config

            if config:
                if config.has_section(task_type):
                    section = config[task_type]
                else:
                    section = config[config.default_section]
                
                # Override domain if present in config and not in ENV
                if not domain:
                    self.worker.domain = section.get("domain", self.worker.domain)

                # Override polling interval if present in config and not in ENV
                if not polling_interval_initialized:
                    # Setting to fallback poll interval before reading config
                    default_polling_interval = self.worker.poll_interval

                    try:
                        # Read polling interval from config
                        self.worker.poll_interval = float(section.get("polling_interval", default_polling_interval))
                        self.logger.debug("Override polling interval to {0} ms".format(self.worker.poll_interval))
                    except Exception as e:
                        self.logger.error("Exception reading polling interval: {0}. Defaulting to {1} ms".format(str(e), default_polling_interval))

    def __get_property_value_from_env(self, prop, task_type):
        prefix = "conductor_worker"
        # Look for generic property in both case environment variables
        key = prefix + "_" + prop
        value_all = os.getenv(key, os.getenv(key.upper()))

        # Look for task specific property in both case environment variables
        key_small = prefix + "_" + task_type + "_" + prop
        key_upper = prefix.upper() + "_" + task_type + "_" + prop.upper()
        value = os.getenv(key_small, os.getenv(key_upper, value_all))
        return value
