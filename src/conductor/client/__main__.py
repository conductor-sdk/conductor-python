from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.sample.simple_python_worker import SimplePythonWorker
import logging

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


def main():
    configuration = Configuration(
        debug=True
    )
    configuration.apply_logging_config()
    workers = [SimplePythonWorker()] * 3
    logger.debug(f'Created workers: {workers}')
    with TaskHandler(configuration, workers) as task_handler:
        logger.debug(f'Created task_handler: {task_handler}')
        task_handler.start()


if __name__ == '__main__':
    main()
