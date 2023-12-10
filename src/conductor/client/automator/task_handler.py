import importlib
import inspect
import logging
import os
from configparser import ConfigParser
from multiprocessing import Process, freeze_support, Queue
from typing import List

from conductor.client.automator.task_runner import TaskRunner
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.metrics_settings import MetricsSettings
from conductor.client.telemetry.metrics_collector import MetricsCollector
from conductor.client.worker.worker import Worker
from conductor.client.worker.worker_interface import WorkerInterface

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)

_decorated_functions = {}


def register_decorated_fn(name: str, func):
    logger.info(f'decorated {name}')
    _decorated_functions[name] = func


class TaskHandler:
    def __init__(
            self,
            workers: List[WorkerInterface] = None,
            configuration: Configuration = None,
            metrics_settings: MetricsSettings = None,
            scan_for_annotated_workers: bool = None,
            import_modules: List[str] = None
    ):
        self.logger_process, self.queue = _setup_logging_queue(configuration)
        self.worker_config = load_worker_config()
        # imports
        importlib.import_module('conductor.client.http.models.task')
        importlib.import_module('conductor.client.worker.worker_task')
        if import_modules is not None:
            for module in import_modules:
                logger.info(f'loading module {module}')
                importlib.import_module(module)

        if workers is None:
            workers = []
        elif not isinstance(workers, list):
            workers = [workers]
        if scan_for_annotated_workers is True:
            for task_def_name in _decorated_functions:
                logger.info(f'{task_def_name} has {_decorated_functions[task_def_name]}')
                worker = Worker(task_definition_name=task_def_name,
                                execute_function=_decorated_functions[task_def_name])
                workers.append(worker)

        self.__create_task_runner_processes(workers, configuration, metrics_settings)
        self.__create_metrics_provider_process(metrics_settings)
        logger.info('TaskHandler initialized')

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
        if metrics_settings is None:
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

    def __create_task_runner_process(
            self,
            worker: WorkerInterface,
            configuration: Configuration,
            metrics_settings: MetricsSettings
    ) -> None:
        task_runner = TaskRunner(worker, configuration, metrics_settings, self.worker_config)
        process = Process(target=task_runner.run)
        self.task_runner_processes.append(process)

    def __start_metrics_provider_process(self):
        if self.metrics_provider_process is None:
            return
        self.metrics_provider_process.start()
        logger.info('Started MetricsProvider process')

    def __start_task_runner_processes(self):
        n = 0
        for task_runner_process in self.task_runner_processes:
            task_runner_process.start()
            n = n + 1
        logger.info(f'Started {n} TaskRunner process')

    def __join_metrics_provider_process(self):
        if self.metrics_provider_process is None:
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
        if process is None:
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
def _setup_logging_queue(configuration: Configuration):
    queue = Queue()
    # logger.addHandler(QueueHandler(queue))
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
