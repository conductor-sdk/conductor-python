from src.http.api.task_resource_api import TaskResourceApi
from src.http.models.task_result import TaskResult
from src.http.rest import ApiException
import logging
import time


class TaskRunner:
    POLLING_INTERVAL = 5

    def __init__(self, worker):
        self.task_client = TaskResourceApi()
        self.worker = worker

    def start(self):
        while True:
            self.__wait()
            task = self.__poll_task(
                self.worker.get_task_definition_name()
            )
            if task != None:
                self.__process_task(task, self.worker)

    def __wait(self):
        logging.debug(f'Sleep for {self.POLLING_INTERVAL} seconds')
        time.sleep(self.POLLING_INTERVAL)

    def __poll_task(self, task_definition_name):
        try:
            return self.task_client.poll(
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

    def __process_task(self, task, worker):
        logging.info(
            'Executing task, id: {task_id}, type: {task_type}, worker: {worker_name}'.format(
                task_id=task.task_id,
                task_type=task.task_type,
                worker_name=worker.get_task_definition_name()
            )
        )
        task_result = TaskResult(
            workflow_instance_id=task._workflow_instance_id,
            task_id=task.task_id
        )
        try:
            self.__execute_task(worker, task_result)
            message = 'Executed task, id: {task_id}, type: {task_type}, worker: {worker_name}'
            logging.info(
                message.format(
                    task_id=task.task_id,
                    task_type=task.task_type,
                    worker_name=worker.get_task_definition_name()
                )
            )
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
                    worker_name=worker.get_task_definition_name(),
                    reason=e
                )
            )
        try:
            self.__update_task(task_result)
            message = 'Updated task, id: {task_id}, type: {task_type}, worker: {worker_name}'
            logging.info(
                message.format(
                    task_id=task.task_id,
                    task_type=task.task_type,
                    worker_name=worker.get_task_definition_name()
                )
            )
        except Exception as e:
            message = (
                'Failed to update task, id: {task_id}'
                ', type: {task_type}, worker: {worker_name}, reason: {reason}'
            )
            logging.warning(
                message.format(
                    task_id=task.task_id,
                    task_type=task.task_type,
                    worker_name=worker.get_task_definition_name(),
                    reason=e
                )
            )

    def __execute_task(self, worker, task_result):
        worker.execute(task_result)
        task_result.status = 'COMPLETED'
        return task_result

    def __update_task(self, task_result):
        return self.task_client.update_task(body=task_result)
