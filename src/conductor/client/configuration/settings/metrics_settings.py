import os
from pathlib import Path


def get_default_temporary_folder() -> str:
    metrics_dir = str(Path.home()) + '/tmp/'
    if not os.path.isdir(metrics_dir):
        os.mkdir(metrics_dir)
    return metrics_dir


class MetricsSettings:
    def __init__(
            self,
            directory: str = get_default_temporary_folder(),
            file_name: str = 'metrics.log',
            update_interval: float = 0.1):
        self.directory = directory
        self.file_name = file_name
        self.update_interval = update_interval
