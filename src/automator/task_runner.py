from src.http.api.task_resource_api import TaskResourceApi
from src.http.models.task import Task
from src.http.models.task_result import TaskResult
from src.http.rest import ApiException
import logging
import time


class TaskRunner:
    POLLING_INTERVAL = 5

    def __init__(self, worker):
        self.worker = worker

    def run(self):
        while True:
            self.__wait()
            task = self.__poll_task()
            self.__process_task(task)

    def __wait(self):
        logging.debug(f'Sleep for {self.POLLING_INTERVAL} seconds')
        time.sleep(self.POLLING_INTERVAL)

    def __poll_task(self):
        task_definition_name = self.worker.get_task_definition_name()
        try:
            # TODO use some kind of task client provider
            return TaskResourceApi().poll(
                tasktype=task_definition_name
            )
        except ApiException as e:
            logging.warning(
                f'Failed to poll task for: {task_definition_name}, ApiException.status: {e.status}'
            )
        except Exception as e:
            logging.warning(
                f'Failed to poll task for: {task_definition_name}, Exception: {e}'
            )
        return None

    def __process_task(self, task):
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
            self.__execute_task(task, task_result)
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
        try:
            return self.__update_task(task, task_result)
        except Exception as e:
            message = (
                'Failed to update task, id: {task_id}'
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

    def __execute_task(self, task, task_result):
        self.worker.execute(task_result)
        task_result.status = 'COMPLETED'
        message = 'Executed task, id: {task_id}, type: {task_type}, worker: {worker_name}'
        logging.info(
            message.format(
                task_id=task.task_id,
                task_type=task.task_type,
                worker_name=self.worker.get_task_definition_name()
            )
        )

    def __update_task(self, task, task_result):
        # TODO use some kind of task client provider
        response = TaskResourceApi().update_task(
            body=task_result
        )
        message = 'Updated task, id: {task_id}, type: {task_type}, worker: {worker_name}'
        logging.info(
            message.format(
                task_id=task.task_id,
                task_type=task.task_type,
                worker_name=self.worker.get_task_definition_name()
            )
        )
        return response
