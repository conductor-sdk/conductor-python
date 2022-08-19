from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.telemetry.counter import *
from conductor.client.telemetry.gauge import *
from typing import List
import logging
import sys
import time
import traceback

_logger = logging.getLogger(__name__)


def run(
    task_resource_api: TaskResourceApi,
    task_name: str,
    poll_interval_in_seconds: float,
    execute_function,
    worker_id: str = None,
    domain: str = None,
) -> None:
    while True:
        try:
            _run_once(
                task_resource_api=task_resource_api,
                task_name=task_name,
                poll_interval_in_seconds=poll_interval_in_seconds,
                execute_function=execute_function,
                worker_id=worker_id,
                domain=domain,
            )
        except Exception as e:
            increment_uncaught_exception()
            _logger.warning(
                'Failed to run once. Reason: {}, task_name: {}, poll_interval: {}, worker_id: {}'.format(
                    str(e),
                    task_name,
                    poll_interval_in_seconds,
                    worker_id,
                )
            )


def _run_once(
    task_resource_api: TaskResourceApi,
    task_name: str,
    poll_interval_in_seconds: float,
    execute_function,
    worker_id: str = None,
    domain: str = None,
) -> None:
    # TODO discover amount of available workers
    available_workers = 1
    tasks = _get_tasks_in_batches(
        task_resource_api=task_resource_api,
        task_name=task_name,
        batch_size=available_workers,
        timeout=poll_interval_in_seconds,
        worker_id=worker_id,
        domain=domain
    )
    if tasks == None or len(tasks) == 0:
        _wait_for_polling_interval(
            poll_interval_in_seconds=poll_interval_in_seconds,
        )
        return
    for task in tasks:
        task_result = _execute_task(
            task=task,
            execute_function=execute_function,
            worker_id=worker_id,

        )
        _update_task(
            task_resource_api=task_resource_api,
            task_name=task_name,
            task_result=task_result,

        )


def _wait_for_polling_interval(poll_interval_in_seconds: float) -> None:
    _logger.debug(f'Sleep for {poll_interval_in_seconds} seconds')
    time.sleep(poll_interval_in_seconds)


def _update_task(
    task_resource_api: TaskResourceApi,
    task_name: str,
    task_result: TaskResult,
) -> None:
    _logger.debug(
        'Updating task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}'.format(
            task_id=task_result.task_id,
            workflow_instance_id=task_result.workflow_instance_id,
            task_definition_name=task_name
        )
    )
    try:
        response = task_resource_api.update_task(
            body=task_result
        )
    except Exception as e:
        increment_task_update_error(
            task_name, type(e)
        )
        _logger.info(
            'Failed to update task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}, reason: {reason}'.format(
                task_id=task_result.task_id,
                workflow_instance_id=task_result.workflow_instance_id,
                task_definition_name=task_name,
                reason=traceback.format_exc()
            )
        )
        return None
    _logger.debug(
        'Updated task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}, response: {response}'.format(
            task_id=task_result.task_id,
            workflow_instance_id=task_result.workflow_instance_id,
            task_definition_name=task_name,
            response=response
        )
    )
    return response


def _get_tasks_in_batches(
    task_resource_api: TaskResourceApi,
    task_name: str,
    batch_size: int,
    # timeout: str,
    worker_id: str = None,
    domain: str = None,
) -> List[Task]:
    kwargs = {
        'count': batch_size,
        # TODO 'timeout': timeout
    }
    if worker_id != None:
        kwargs['workerid'] = worker_id
    if domain != None:
        kwargs['domain'] = domain
    increment_task_poll(task_name)
    try:
        start_time = time.time()
        tasks = task_resource_api.batch_poll(task_name, **kwargs)
        finish_time = time.time()
        time_spent = finish_time - start_time
        record_task_poll_time(task_name, time_spent)
    except Exception as e:
        increment_task_poll_error(
            task_name, type(e)
        )
        _logger.info(
            f'Failed to poll task for: {task_name}, reason: {traceback.format_exc()}'
        )
        return None
    if tasks != None:
        _logger.debug(
            'Polled {} task(s) for: {} with worker_id: {}'.format(
                len(tasks), task_name, worker_id
            )
        )
    return tasks


def _execute_task(
    task: Task,
    execute_function,  # TODO add type guide
    worker_id: str = None,
) -> TaskResult:
    _logger.debug(
        'Executing task, id: {}, workflow_instance_id: {}, task_definition_name: {}'.format(
            task.task_id, task.workflow_instance_id, task.task_def_name
        )
    )
    try:
        start_time = time.time()
        task_result = execute_function(task)
        finish_time = time.time()
        time_spent = finish_time - start_time
        record_task_execute_time(
            task.task_def_name, time_spent,
        )
        record_task_result_payload_size(
            task.task_def_name, sys.getsizeof(task_result),
        )
        _logger.debug(
            'Executed task, id: {}, workflow_instance_id: {}, task_definition_name: {}'.format(
                task.task_id, task.workflow_instance_id, task.task_def_name
            )
        )
    except Exception as e:
        increment_task_execution_error(
            task.task_id, type(e),
        )
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id=worker_id,
        )
        task_result.status = TaskResultStatus.FAILED
        task_result.reason_for_incompletion = str(e)
        _logger.info(
            'Failed to execute task, id: {}, workflow_instance_id: {}, task_definition_name: {}, reason: {}'.format(
                task.task_id,
                task.workflow_instance_id,
                task.task_def_name,
                traceback.format_exc(),
            )
        )
    return task_result
