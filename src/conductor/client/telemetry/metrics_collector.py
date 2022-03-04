from conductor.client.configuration.configuration import Configuration
from prometheus_client import CollectorRegistry, Gauge
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
        self.task_poll_counter = Counter(
            name='task_poll',
            documentation='Number of times the task has been polled',
            registry=self.registry
        )
        self.task_poll_error_counter = Counter(
            name='task_poll_error',
            documentation='Number of times the task has been polled, when the worker has been paused',
            registry=self.registry
        )
        self.task_paused_counter = Counter(
            name='task_paused',
            documentation='Number of times the task has been polled, when the worker has been paused',
            registry=self.registry
        )
        self.task_execute_error_counter = Counter(
            name='task_execute_error',
            documentation='Number of times the task has been executed with an error',
            registry=self.registry
        )
        self.task_update_error_counter = Counter(
            name='task_update_error',
            documentation='Number of times the task has been updated with an error',
            registry=self.registry
        )
        self.task_poll_time_gauge = Gauge(
            name='task_poll_time',
            documentation='Time to poll for a task',
            registry=self.registry
        )
        self.task_execute_time_gauge = Gauge(
            name='task_execute_time',
            documentation='Time to execute a task',
            registry=self.registry
        )
        self.task_result_size_gauge = Gauge(
            name='task_result_size',
            documentation='Size of TaskResult',
            registry=self.registry
        )
        self.external_payload_used_counter = Counter(
            name='external_payload_used',
            documentation='Size of TaskResult',
            registry=self.registry
        )
        # task_execution_queue_full
        # task_ack_failed
        # task_ack_error
        # workflow_input_size

    # def increment_counter(self):
    #     self.counter.inc()
