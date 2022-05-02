from conductor.client.configuration.configuration import Configuration
from pathlib import Path
import logging
import os

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


def get_default_temporary_folder() -> str:
    try:
        metrics_dir = str(Path.home()) + '/tmp/'
        if not os.path.isdir(metrics_dir):
            os.mkdir(metrics_dir)
        return metrics_dir
    except Exception as e:
        logger.warning('Failed to create metrics temporary folder')


class MetricsSettings:
    def __init__(
            self,
            directory: str = None,
            file_name: str = 'metrics.log',
            update_interval: float = 0.1):
        if directory == None:
            directory = get_default_temporary_folder()
        if not os.path.isdir(directory):
            raise Exception(
                f'Failed to set metrics directory to: {directory}, reason: folder does not exists'
            )
        self.directory = directory
        self.file_name = file_name
        self.update_interval = update_interval
