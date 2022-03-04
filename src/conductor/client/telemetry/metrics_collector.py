from conductor.client.configuration.configuration import Configuration
from prometheus_client import CollectorRegistry
from prometheus_client import Counter
from prometheus_client.multiprocess import MultiProcessCollector
import os


class MetricsCollector:
    def __init__(self):
        # TODO improve this hard coded ENV
        os.environ["PROMETHEUS_MULTIPROC_DIR"] = Configuration.METRICS_PREFIX_DIR
        self.registry = CollectorRegistry()
        MultiProcessCollector(self.registry)
        self.__create_counters()

    def __create_counters(self):
        self.counter = Counter(
            'counter',
            'counter sample',
            registry=self.registry
        )

    def increment_counter(self):
        self.counter.inc()
