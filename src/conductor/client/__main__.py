from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.simple_python_worker import SimplePythonWorker
import logging
import os

logger = logging.getLogger(
    '.'.join(
        [
            str(os.getpid()),
            __name__
        ]
    )
)


def main():
    configuration = Configuration(
        debug=True
    )
    configuration.apply_logging_config()

    workers = [SimplePythonWorker()] * 20
    logger.info(f'Created {len(workers)} workers: {workers}')
    with TaskHandler(configuration, workers) as task_handler:
        logger.info('Created TaskHandler')
        task_handler.start()


if __name__ == '__main__':
    main()
