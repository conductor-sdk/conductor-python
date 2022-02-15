from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.api_client import ApiClient
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.rest import ApiException
import logging
import os
import time


logger = logging.getLogger(
    '.'.join(
        [
            str(os.getpid()),
            __name__
        ]
    )
)


class TaskRunner:
    def __init__(self, configuration, worker):
        self.configuration = configuration
        self.worker = worker

    def run(self):
        self.configuration.apply_logging_config()
        while True:
            task = self.__poll_task()
            if task is not None:
                task_result = self.__execute_task(task)
                self.__update_task(task_result)
                self.__wait_for_polling_interval()

    def __poll_task(self):
        task_definition_name = self.worker.get_task_definition_name()
        logger.debug(f'Polling task for: {task_definition_name}')
        try:
            task = TaskResourceApi(ApiClient(configuration=self.configuration)).poll(
                tasktype=task_definition_name
            )
        except Exception as e:
            return None
        message = 'Polled task for worker: {task_definition_name}, identity: {identity}'
        logger.debug(
            message.format(
                task_definition_name=task_definition_name,
                identity=self.worker.get_identity()
            )
        )
        return task

    def __execute_task(self, task):
        if isinstance(task, Task) == False:
            return None
        logger.info(
            'Executing task, id: {task_id}, type: {task_type}, worker: {worker_name}'.format(
                task_id=task.task_id,
                task_type=task.task_type,
                worker_name=self.worker.get_task_definition_name()
            )
        )
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id=self.worker.get_task_definition_name()
        )
        try:
            self.worker.execute(task)
            task_result.status = 'COMPLETED'
            task_result.output_data = task.output_data
            return task_result
        except Exception as e:
            task_result.status = 'FAILED'
            message = (
                'Failed to execute task, id: {task_id}'
                ', type: {task_type}, worker: {worker_name}, reason: {reason}'
            )
            logger.warning(
                message.format(
                    task_id=task.task_id,
                    task_type=task.task_type,
                    worker_name=self.worker.get_task_definition_name(),
                    reason=e
                )
            )
            return None
        message = 'Executed task, id: {task_id}, type: {task_type}, worker: {worker_name}'
        logger.info(
            message.format(
                task_id=task.task_id,
                task_type=task.task_type,
                worker_name=self.worker.get_task_definition_name()
            )
        )

    def __update_task(self, task_result):
        logger.debug('updating task: {}, status: {}'.format(task_result.task_id, task_result.status))
        if isinstance(task_result, TaskResult) == False:
            return None
        try:
            response = TaskResourceApi(ApiClient(configuration=self.configuration)).update_task(
                body=task_result
            )
        except Exception as e:
            message = (
                'Failed to update task, id: {task_id}'
                ', type: {task_type}, worker: {worker_name}, reason: {reason}'
            )
            logger.warning(
                message.format(
                    task_id=task_result.task_id,
                    task_type=task_result.task_type,
                    worker_name=self.worker.get_task_definition_name(),
                    reason=e
                )
            )
            return None
        message = 'Updated task, id: {task_id}, worker: {worker_name}, response: {response}'
        logger.info(
            message.format(
                task_id=task_result.task_id,
                worker_name=self.worker.get_task_definition_name(),
                response=response
            )
        )
        return response

    def __wait_for_polling_interval(self):
        polling_interval = self.worker.get_polling_interval()
        logger.debug(f'Sleep for {polling_interval} seconds')
        time.sleep(polling_interval)
