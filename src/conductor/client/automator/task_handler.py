from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.telemetry.metrics_collector import MetricsCollector
from conductor.client.worker.worker import Worker
from conductor.client.worker.worker_interface import WorkerInterface
from conductor.client.worker.worker_task import WorkerTask
from multiprocessing import Process, freeze_support
from typing import List
import ast
import inspect
import logging
import os
import copy

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


def get_annotated_workers():
    pkg = __get_client_topmost_package_filepath()
    workers = __get_annotated_workers_from_subtree(pkg)
    logger.debug(f'Found {len(workers)} workers')
    return workers


class TaskHandler:
    def __init__(
            self,
            workers: List[WorkerInterface],
            configuration: Configuration = None,
            metrics_settings: MetricsSettings = None,
            scan_for_annotated_workers: bool = None,
    ):
        if not isinstance(workers, list):
            workers = [workers]
        if scan_for_annotated_workers is not False:
            for worker in get_annotated_workers():
                workers.append(worker)
        self.__create_task_runner_processes(
            workers, configuration, metrics_settings
        )
        self.__create_metrics_provider_process(
            metrics_settings
        )
        logger.info('Created all processes')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_processes()

    def stop_processes(self) -> None:
        self.__stop_task_runner_processes()
        self.__stop_metrics_provider_process()
        logger.debug('stopped processes')

    def start_processes(self) -> None:
        logger.info('Starting worker processes...')
        freeze_support()
        self.__start_task_runner_processes()
        self.__start_metrics_provider_process()
        logger.info('Started all processes')

    def join_processes(self) -> None:
        self.__join_task_runner_processes()
        self.__join_metrics_provider_process()
        logger.info('Joined all processes')

    def __create_metrics_provider_process(self, metrics_settings: MetricsSettings) -> None:
        if metrics_settings == None:
            self.metrics_provider_process = None
            return
        self.metrics_provider_process = Process(
            target=MetricsCollector.provide_metrics,
            args=(metrics_settings,)
        )
        logger.info('Created MetricsProvider process')

    def __create_task_runner_processes(
        self,
        workers: List[WorkerInterface],
        configuration: Configuration,
        metrics_settings: MetricsSettings
    ) -> None:
        self.task_runner_processes = []
        for worker in workers:
            self.__create_task_runner_process(
                worker, configuration, metrics_settings
            )
        logger.info('Created TaskRunner processes')

    def __create_task_runner_process(
        self,
        worker: WorkerInterface,
        configuration: Configuration,
        metrics_settings: MetricsSettings
    ) -> None:
        task_runner = TaskRunner(worker, configuration, metrics_settings)
        process = Process(
            target=task_runner.run
        )
        self.task_runner_processes.append(process)

    def __start_metrics_provider_process(self):
        if self.metrics_provider_process == None:
            return
        self.metrics_provider_process.start()
        logger.info('Started MetricsProvider process')

    def __start_task_runner_processes(self):
        for task_runner_process in self.task_runner_processes:
            task_runner_process.start()
        logger.info('Started TaskRunner processes')

    def __join_metrics_provider_process(self):
        if self.metrics_provider_process == None:
            return
        self.metrics_provider_process.join()
        logger.info('Joined MetricsProvider processes')

    def __join_task_runner_processes(self):
        for task_runner_process in self.task_runner_processes:
            task_runner_process.join()
        logger.info('Joined TaskRunner processes')

    def __stop_metrics_provider_process(self):
        self.__stop_process(self.metrics_provider_process)

    def __stop_task_runner_processes(self):
        for task_runner_process in self.task_runner_processes:
            self.__stop_process(task_runner_process)

    def __stop_process(self, process: Process):
        if process == None:
            return
        try:
            process.kill()
            logger.debug(f'Killed process: {process}')
        except Exception as e:
            logger.debug(f'Failed to kill process: {process}, reason: {e}')
            process.terminate()
            logger.debug('Terminated process: {process}')


def __get_client_topmost_package_filepath():
    module = inspect.getmodule(inspect.stack()[-1][0])
    while module:
        if not getattr(module, '__parent__', None):
            logger.debug(f'parent module not found for {module}')
            return getattr(module, '__file__', None)
        module = getattr(module, '__parent__', None)
    return None


def __get_annotated_workers_from_subtree(pkg):
    workers = []
    if not pkg:
        return workers
    pkg_path = os.path.dirname(pkg)
    for root, _, files in os.walk(pkg_path):
        for file in files:
            if not file.endswith('.py') or file == '__init__.py':
                continue
            module_path = os.path.join(root, file)
            with open(module_path, 'r') as file:
                source_code = file.read()
            module = ast.parse(source_code, filename=module_path)
            for node in ast.walk(module):
                if not isinstance(node, ast.FunctionDef):
                    continue
                for decorator in node.decorator_list:
                    decorator_type, params = __extract_decorator_info(
                        decorator)
                    if decorator_type != 'WorkerTask':
                        continue
                    try:
                        worker = __create_worker_from_ast_node(
                            node, params)
                        if worker:
                            workers.append(worker)
                    except Exception as e:
                        logger.debug(
                            f'Failed to create worker from function: {node.name}. Reason: {str(e)}')
                        continue
    return workers


def __extract_decorator_info(decorator):
    if not isinstance(decorator, ast.Call):
        return None, None
    decorator_type = None
    decorator_params = {}
    decorator_func = decorator.func
    if isinstance(decorator_func, ast.Attribute):
        decorator_type = decorator_func.attr
    elif isinstance(decorator_func, ast.Name):
        decorator_type = decorator_func.id
    if decorator.keywords:
        for keyword in decorator.keywords:
            param_name = keyword.arg
            param_value = keyword.value.value
            decorator_params[param_name] = param_value
    return decorator_type, decorator_params


def __create_worker_from_ast_node(node, params):
    auxiliar_node = copy.deepcopy(node)
    auxiliar_node.decorator_list = []
    function_source_code = ast.unparse(auxiliar_node)
    exec(function_source_code)
    execute_function = locals()[node.name]
    params['execute_function'] = execute_function
    worker = Worker(**params)
    return worker
