from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.telemetry.metrics_collector import MetricsCollector
from conductor.client.worker.worker import Worker
from conductor.client.worker.worker_interface import WorkerInterface
from multiprocessing import Process, freeze_support, Queue
from configparser import ConfigParser
from logging.handlers import QueueHandler
from typing import List
import ast
import astor
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
            workers: List[WorkerInterface] = None,
            configuration: Configuration = None,
            metrics_settings: MetricsSettings = None,
            scan_for_annotated_workers: bool = None,
    ):
        self.logger_process, self.queue = setup_logging_queue(configuration)
        self.worker_config = load_worker_config()
        if workers is None:
            workers = []
        elif not isinstance(workers, list):
            workers = [workers]
        if scan_for_annotated_workers is True:
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
        logger.info('Stopped worker processes...')
        logger.info('Stopping logger process...')
        self.queue.put(None)
        self.logger_process.terminate()

    def start_processes(self) -> None:
        logger.info('Starting worker processes...')
        freeze_support()
        self.__start_task_runner_processes()
        self.__start_metrics_provider_process()
        logger.info('Started all processes')

    def join_processes(self) -> None:
        try:
            self.__join_task_runner_processes()
            self.__join_metrics_provider_process()
            logger.info('Joined all processes')
        except KeyboardInterrupt:
            logger.info('KeyboardInterrupt: Stopping all processes')
            self.stop_processes()

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
        task_runner = TaskRunner(
            worker, configuration, metrics_settings, self.worker_config
        )
        process = Process(
            target=task_runner.run, args=(self.queue,)
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
            logger.debug(f'Terminating process: {process.pid}')
            process.terminate()
        except Exception as e:
            logger.debug(f'Failed to terminate process: {process.pid}, reason: {e}')
            process.kill()
            logger.debug(f'Killed process: {process.pid}')

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
                    params = __extract_decorator_info(
                        decorator)
                    if params is None:
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
    decorator_func = decorator.func
    if isinstance(decorator_func, ast.Attribute):
        decorator_type = decorator_func.attr
    elif isinstance(decorator_func, ast.Name):
        decorator_type = decorator_func.id
    if decorator_type != 'WorkerTask':
        return None
    decorator_params = {}
    if decorator.args:
        for arg in decorator.args:
            arg_value = astor.to_source(arg).strip()
            decorator_params[arg_value] = ast.literal_eval(arg)
    if decorator.keywords:
        for keyword in decorator.keywords:
            param_name = keyword.arg
            param_value = ast.literal_eval(keyword.value)
            decorator_params[param_name] = param_value
    return decorator_params


def __create_worker_from_ast_node(node, params):
    auxiliar_node = copy.deepcopy(node)
    auxiliar_node.decorator_list = []
    function_source_code = ast.unparse(auxiliar_node)
    exec(function_source_code)
    execute_function = locals()[node.name]
    params['execute_function'] = execute_function
    worker = Worker(**params)
    return worker

def load_worker_config():
    worker_config = ConfigParser()

    try:
        file = __get_config_file_path()
        worker_config.read(file)
    except Exception as e:
        logger.error(str(e))

    return worker_config

def __get_config_file_path() -> str:
    return os.getcwd() + "/worker.ini"

# Setup centralized logging queue
def setup_logging_queue(configuration):
    queue = Queue()
    logger.addHandler(QueueHandler(queue))
    if configuration:
        configuration.apply_logging_config()
        log_level = configuration.log_level
        logger_format = configuration.logger_format
    else:
        log_level = logging.DEBUG
        logger_format = None
    
    logger.setLevel(log_level)
    
    # start the logger process
    logger_p = Process(target=__logger_process, args=(queue, log_level, logger_format))
    logger_p.start()
    return logger_p, queue

# This process performs the centralized logging
def __logger_process(queue, log_level, logger_format=None):
    c_logger = logging.getLogger(
        Configuration.get_logging_formatted_name(
            __name__
        )
    )
    
    c_logger.setLevel(log_level)
        
    # configure a stream handler
    sh = logging.StreamHandler()
    if logger_format:
        formatter = logging.Formatter(logger_format)
        sh.setFormatter(formatter)
    c_logger.addHandler(sh)
    
    # run forever
    while True:
        # consume a log message, block until one arrives
        message = queue.get()
        # check for shutdown
        if message is None:
            break
        # log the message
        c_logger.handle(message)