from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.rest import ApiException
import logging
import time


class TaskRunner:
    def __init__(self, worker):
        self.worker = worker

    def run(self):
        while True:
            task = self.__poll_task()
            task_result = self.__execute_task(task)
            self.__update_task(task_result)
            self.__wait_for_polling_interval()

    def __poll_task(self):
        task_definition_name = self.worker.get_task_definition_name()
        logging.debug(f'Polling task for: {task_definition_name}')
        try:
            task = TaskResourceApi().poll(
                tasktype=task_definition_name
            )
        except ApiException as e:
            logging.warning(
                f'Failed to poll task for: {task_definition_name}, ApiException.status: {e.status}'
            )
            return None
        message = 'Polled task for worker: {task_definition_name}, identity: {identity}'
        logging.debug(
            message.format(
                task_definition_name=task_definition_name,
                identity=self.worker.get_identity()
            )
        )
        return task

    def __execute_task(self, task):
        if isinstance(task, Task) == False:
            return None
        logging.info(
            'Executing task, id: {task_id}, type: {task_type}, worker: {worker_name}'.format(
                task_id=task.task_id,
                task_type=task.task_type,
                worker_name=self.worker.get_task_definition_name()
            )
        )
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id
        )
        try:
            self.worker.execute(task_result)
            task_result.status = 'COMPLETED'
        except Exception as e:
            task_result.status = 'FAILED'
            message = (
                'Failed to execute task, id: {task_id}'
                ', type: {task_type}, worker: {worker_name}, reason: {reason}'
            )
            logging.warning(
                message.format(
                    task_id=task.task_id,
                    task_type=task.task_type,
                    worker_name=self.worker.get_task_definition_name(),
                    reason=e
                )
            )
            return None
        message = 'Executed task, id: {task_id}, type: {task_type}, worker: {worker_name}'
        logging.info(
            message.format(
                task_id=task.task_id,
                task_type=task.task_type,
                worker_name=self.worker.get_task_definition_name()
            )
        )

    def __update_task(self, task_result):
        if isinstance(task_result, TaskResult) == False:
            return None
        try:
            response = TaskResourceApi().update_task(
                body=task_result
            )
        except Exception as e:
            message = (
                'Failed to update task, id: {task_id}'
                ', type: {task_type}, worker: {worker_name}, reason: {reason}'
            )
            logging.warning(
                message.format(
                    task_id=task_result.task_id,
                    task_type=task_result.task_type,
                    worker_name=self.worker.get_task_definition_name(),
                    reason=e
                )
            )
            return None
        message = 'Updated task, id: {task_id}, type: {task_type}, worker: {worker_name}, response: {response}'
        logging.info(
            message.format(
                task_id=task_result.task_id,
                task_type=task_result.task_type,
                worker_name=self.worker.get_task_definition_name(),
                response=response
            )
        )
        return response

    def __wait_for_polling_interval(self):
        polling_interval = self.worker.get_polling_interval()
        logging.debug(f'Sleep for {polling_interval} seconds')
        time.sleep(polling_interval)
