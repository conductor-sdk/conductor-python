from conductor.client.configuration.configuration import Configuration
from prometheus_client import CollectorRegistry
from prometheus_client import write_to_textfile
from prometheus_client.multiprocess import MultiProcessCollector
import logging
import os
import time

logger = logging.getLogger(
    Configuration.get_logging_formatted_name(
        __name__
    )
)


def provide_metrics():
    OUTPUT_FILE_PATH = os.path.join(
        Configuration.METRICS_PREFIX_DIR, 'latest.txt'
    )
    registry = CollectorRegistry()
    MultiProcessCollector(registry)
    while True:
        write_to_textfile(
            OUTPUT_FILE_PATH,
            registry
        )
        time.sleep(0.1)
