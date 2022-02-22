from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.worker.worker_interface import WorkerInterface
import logging
import time

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


class TaskRunner:
    def __init__(self, worker: WorkerInterface, configuration: Configuration = None):
        if configuration != None and not isinstance(configuration, Configuration):
            raise Exception('Invalid configuration')
        if not isinstance(worker, WorkerInterface):
            raise Exception('Invalid worker')
        self.configuration = configuration
        self.worker = worker

    def run(self) -> None:
        if self.configuration != None:
            self.configuration.apply_logging_config()
        while True:
            self.run_once()

    def run_once(self) -> None:
        task = self.__poll_task()
        if task != None:
            task_result = self.__execute_task(task)
            self.__update_task(task_result)
        self.__wait_for_polling_interval()

    def __poll_task(self) -> Task:
        task_definition_name = self.worker.get_task_definition_name()
        logger.info(f'Polling task for: {task_definition_name}')
        try:
            task = self.__get_task_resource_api().poll(
                tasktype=task_definition_name
            )
        except Exception:
            return None
        message = 'Polled task for worker: {task_definition_name}, identity: {identity}'
        logger.debug(
            message.format(
                task_definition_name=task_definition_name,
                identity=self.worker.get_identity()
            )
        )
        return task

    def __execute_task(self, task: Task) -> TaskResult:
        if not isinstance(task, Task):
            return None
        logger.info(
            'Executing task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, worker: {worker_name}'.format(
                task_id=task.task_id,
                workflow_instance_id=task.workflow_instance_id,
                worker_name=self.worker.get_task_definition_name()
            )
        )
        try:
            task_result = self.worker.execute(task)
            logger.info(
                'Executed task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, worker: {worker_name}'.format(
                    task_id=task.task_id,
                    workflow_instance_id=task.workflow_instance_id,
                    worker_name=self.worker.get_task_definition_name()
                )
            )
        except Exception as e:
            task_result = TaskResult(
                task_id=task.task_id,
                workflow_instance_id=task.workflow_instance_id,
                worker_id=self.worker.get_task_definition_name()
            )
            task_result.status = 'FAILED'
            task_result.reason_for_incompletion = str(e)
            logger.warning(
                'Failed to execute task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, worker: {worker_name}, reason: {reason}'.format(
                    task_id=task.task_id,
                    workflow_instance_id=task.workflow_instance_id,
                    worker_name=self.worker.get_task_definition_name(),
                    reason=str(e)
                )
            )
        return task_result

    def __update_task(self, task_result: TaskResult):
        if not isinstance(task_result, TaskResult):
            return None
        logger.debug(
            'Updating task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, worker: {worker_name}'.format(
                task_id=task_result.task_id,
                workflow_instance_id=task_result.workflow_instance_id,
                worker_name=self.worker.get_task_definition_name()
            )
        )
        try:
            response = self.__get_task_resource_api().update_task(
                body=task_result
            )
        except Exception as e:
            logger.warning(
                'Failed to update task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, worker: {worker_name}, reason: {reason}'.format(
                    task_id=task_result.task_id,
                    workflow_instance_id=task_result.workflow_instance_id,
                    worker_name=self.worker.get_task_definition_name(),
                    reason=str(e)
                )
            )
            return None
        logger.info(
            'Updated task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, worker: {worker_name}, response: {response}'.format(
                task_id=task_result.task_id,
                workflow_instance_id=task_result.workflow_instance_id,
                worker_name=self.worker.get_task_definition_name(),
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
