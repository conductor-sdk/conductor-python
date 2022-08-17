from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.http.api_client import ApiClient
from conductor.client.http.api.task_resource_api import TaskResourceApi
from conductor.client.http.models.task import Task
from conductor.client.http.models.task_result import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.telemetry.metrics_collector import MetricsCollector
from conductor.client.worker.worker_interface import WorkerInterface
from typing import List
import logging
import sys
import time
import traceback

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


def run(
    configuration: Configuration,
    task_name: str,
    poll_interval_in_seconds: float,
    execute_function,
    worker_id: str = None,
    domain: str = None,
    metrics_collector: MetricsCollector = None,
) -> None:
    configuration.apply_logging_config()
    while True:
        try:
            run_once(
                configuration=configuration,
                task_name=task_name,
                poll_interval_in_seconds=poll_interval_in_seconds,
                execute_function=execute_function,
                worker_id=worker_id,
                domain=domain,
                metrics_collector=metrics_collector
            )
        except Exception as e:
            if metrics_collector != None:
                metrics_collector.increment_uncaught_exception()
            logger.warning(
                'Failed to run once. Reason: {}, task_name: {}, poll_interval: {}, worker_id: {}'.format(
                    str(e),
                    task_name,
                    poll_interval_in_seconds,
                    worker_id,
                )
            )


def run_once(
    configuration: Configuration,
    task_name: str,
    poll_interval_in_seconds: float,
    execute_function,
    worker_id: str = None,
    domain: str = None,
    metrics_collector: MetricsCollector = None,
) -> None:
    # TODO discover amount of available workers
    available_workers = 1
    tasks = get_tasks_in_batches(
        configuration=configuration,
        task_name=task_name,
        batch_size=available_workers,
        timeout=poll_interval_in_seconds,
        worker_id=worker_id,
        domain=domain
    )
    if tasks == None or len(tasks) == 0:
        wait_for_polling_interval(
            poll_interval_in_seconds=poll_interval_in_seconds,
        )
        return
    for task in tasks:
        task_result = execute_task(
            task=task,
            execute_function=execute_function,
            worker_id=worker_id,
            metrics_collector=metrics_collector,
        )
        update_task(
            configuration=configuration,
            task_name=task_name,
            task_result=task_result,
            metrics_collector=metrics_collector,
        )


def wait_for_polling_interval(poll_interval_in_seconds: float) -> None:
    logger.debug(f'Sleep for {poll_interval_in_seconds} seconds')
    time.sleep(poll_interval_in_seconds)


def get_task_resource_api(configuration: Configuration) -> TaskResourceApi:
    return TaskResourceApi(
        ApiClient(
            configuration
        )
    )


def update_task(
    configuration: Configuration,
    task_name: str,
    task_result: TaskResult,
    metrics_collector: MetricsCollector = None,
) -> None:
    logger.debug(
        'Updating task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}'.format(
            task_id=task_result.task_id,
            workflow_instance_id=task_result.workflow_instance_id,
            task_definition_name=task_name
        )
    )
    task_resource_api = get_task_resource_api(configuration)
    try:
        response = task_resource_api.update_task(
            body=task_result
        )
    except Exception as e:
        if metrics_collector != None:
            metrics_collector.increment_task_update_error(
                task_name, type(e)
            )
        logger.info(
            'Failed to update task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}, reason: {reason}'.format(
                task_id=task_result.task_id,
                workflow_instance_id=task_result.workflow_instance_id,
                task_definition_name=task_name,
                reason=traceback.format_exc()
            )
        )
        return None
    logger.debug(
        'Updated task, id: {task_id}, workflow_instance_id: {workflow_instance_id}, task_definition_name: {task_definition_name}, response: {response}'.format(
            task_id=task_result.task_id,
            workflow_instance_id=task_result.workflow_instance_id,
            task_definition_name=task_name,
            response=response
        )
    )
    return response


def get_tasks_in_batches(
    configuration: Configuration,
    task_name: str,
    batch_size: int,
    timeout: str,
    worker_id: str = None,
    domain: str = None,
    metrics_collector: MetricsCollector = None,
) -> List[Task]:
    kwargs = {
        'count': batch_size,
        # TODO 'timeout': timeout
    }
    if worker_id != None:
        kwargs['workerid'] = worker_id
    if domain != None:
        kwargs['domain'] = domain
    if metrics_collector != None:
        metrics_collector.increment_task_poll(task_name)
    task_resource_api = get_task_resource_api(configuration)
    try:
        start_time = time.time()
        tasks = task_resource_api.batch_poll(task_name, **kwargs)
        finish_time = time.time()
        time_spent = finish_time - start_time
        if metrics_collector != None:
            metrics_collector.record_task_poll_time(task_name, time_spent)
    except Exception as e:
        if metrics_collector != None:
            metrics_collector.increment_task_poll_error(
                task_name, type(e)
            )
        logger.info(
            f'Failed to poll task for: {task_name}, reason: {traceback.format_exc()}'
        )
        return None
    if tasks != None:
        logger.debug(
            'Polled {} task(s) for: {} with worker_id: {}'.format(
                len(tasks), task_name, worker_id
            )
        )
    return tasks


def execute_task(
    task: Task,
    execute_function,  # TODO add type guide
    worker_id: str = None,
    metrics_collector: MetricsCollector = None,
) -> TaskResult:
    logger.debug(
        'Executing task, id: {}, workflow_instance_id: {}, task_definition_name: {}'.format(
            task.task_id, task.workflow_instance_id, task.task_def_name
        )
    )
    try:
        start_time = time.time()
        task_result = execute_function(task)
        finish_time = time.time()
        time_spent = finish_time - start_time
        if metrics_collector != None:
            metrics_collector.record_task_execute_time(
                task.task_def_name, time_spent,
            )
            metrics_collector.record_task_result_payload_size(
                task.task_def_name, sys.getsizeof(task_result),
            )
        logger.debug(
            'Executed task, id: {}, workflow_instance_id: {}, task_definition_name: {}'.format(
                task.task_id, task.workflow_instance_id, task.task_def_name
            )
        )
    except Exception as e:
        if metrics_collector != None:
            metrics_collector.increment_task_execution_error(
                task.task_id, type(e),
            )
        task_result = TaskResult(
            task_id=task.task_id,
            workflow_instance_id=task.workflow_instance_id,
            worker_id=worker_id,
        )
        task_result.status = TaskResultStatus.FAILED
        task_result.reason_for_incompletion = str(e)
        logger.info(
            'Failed to execute task, id: {}, workflow_instance_id: {}, task_definition_name: {}, reason: {}'.format(
                task.task_id,
                task.workflow_instance_id,
                task.task_def_name,
                traceback.format_exc(),
            )
        )
    return task_result


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
        self.metrics_collector = MetricsCollector(
            metrics_settings
        )
