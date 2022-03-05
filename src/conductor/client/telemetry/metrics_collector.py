from conductor.client.configuration.configuration import Configuration
from conductor.client.telemetry.model.metric_documentation import MetricDocumentation
from conductor.client.telemetry.model.metric_label import MetricLabel
from conductor.client.telemetry.model.metric_name import MetricName
from prometheus_client import CollectorRegistry
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client.multiprocess import MultiProcessCollector
from typing import List
import os


class MetricsCollector:
    counters = {}
    registry = CollectorRegistry()

    def __init__(self):
        # TODO improve hard coded ENV
        os.environ["PROMETHEUS_MULTIPROC_DIR"] = Configuration.METRICS_PREFIX_DIR
        MultiProcessCollector(self.registry)

    def increment_task_poll_counter(self, task_type: str) -> None:
        counter = self.__get_counter(
            name=MetricName.TASK_POLL,
            documentation=MetricDocumentation.TASK_POLL,
            labelnames=[
                MetricLabel.TASK_TYPE
            ]
        )
        self.__increment_counter(counter, [task_type])

    def __increment_counter(self, counter: Counter, label_values: List[MetricLabel]) -> None:
        counter.labels(*label_values).inc()

    def __get_counter(
        self,
        name: MetricName,
        documentation: MetricDocumentation,
        labelnames: List[MetricLabel]
    ) -> Counter:
        if name not in self.counters:
            self.counters[name] = self.__generate_counter(
                name, documentation, labelnames
            )
        return self.counters[name]

    def __generate_counter(
        self,
        name: MetricName,
        documentation: MetricDocumentation,
        labelnames: List[MetricLabel]
    ) -> Counter:
        return Counter(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            registry=self.registry
        )
