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

    def increment_task_execution_queue_full_counter(self, task_type: str) -> None:
        counter = self.__get_counter(
            name=MetricName.TASK_EXECUTION_QUEUE_FULL,
            documentation=MetricDocumentation.TASK_EXECUTION_QUEUE_FULL,
            labelnames=[
                MetricLabel.TASK_TYPE
            ]
        )
        self.__increment_counter(counter, [task_type])

    # public static void incrementUncaughtExceptionCount() {
    #     incrementCount(THREAD_UNCAUGHT_EXCEPTION);
    # }

    def increment_task_poll_error_counter(self, task_type: str, exception: Exception) -> None:
        counter = self.__get_counter(
            name=MetricName.TASK_POLL_ERROR,
            documentation=MetricDocumentation.TASK_POLL_ERROR,
            labelnames=[
                MetricLabel.TASK_TYPE,
                MetricLabel.EXCEPTION
            ]
        )
        self.__increment_counter(counter, [task_type, str(exception)])

    def increment_task_paused_counter(self, task_type: str) -> None:
        counter = self.__get_counter(
            name=MetricName.TASK_PAUSED,
            documentation=MetricDocumentation.TASK_PAUSED,
            labelnames=[
                MetricLabel.TASK_TYPE
            ]
        )
        self.__increment_counter(counter, [task_type])

    # public static void incrementTaskExecutionErrorCount(String taskType, Throwable e) {
    #     incrementCount(
    #             TASK_EXECUTE_ERROR, TASK_TYPE, taskType, EXCEPTION, e.getClass().getSimpleName());
    # }

    def increment_task_ack_failed_counter(self, task_type: str) -> None:
        counter = self.__get_counter(
            name=MetricName.TASK_ACK_FAILED,
            documentation=MetricDocumentation.TASK_ACK_FAILED,
            labelnames=[
                MetricLabel.TASK_TYPE
            ]
        )
        self.__increment_counter(counter, [task_type])

    # public static void incrementTaskAckErrorCount(String taskType, Exception e) {
    #     incrementCount(
    #             TASK_ACK_ERROR, TASK_TYPE, taskType, EXCEPTION, e.getClass().getSimpleName());
    # }

    # public static void recordTaskResultPayloadSize(String taskType, long payloadSize) {
    #     getGauge(TASK_RESULT_SIZE, TASK_TYPE, taskType).getAndSet(payloadSize);
    # }

    # public static void incrementTaskUpdateErrorCount(String taskType, Throwable t) {
    #     incrementCount(
    #             TASK_UPDATE_ERROR, TASK_TYPE, taskType, EXCEPTION, t.getClass().getSimpleName());
    # }

    # public static void recordWorkflowInputPayloadSize(
    #         String workflowType, String version, long payloadSize) {
    #     getGauge(WORKFLOW_INPUT_SIZE, WORKFLOW_TYPE, workflowType, WORKFLOW_VERSION, version)
    #             .getAndSet(payloadSize);
    # }

    # public static void incrementExternalPayloadUsedCount(
    #         String name, String operation, String payloadType) {
    #     incrementCount(
    #             EXTERNAL_PAYLOAD_USED,
    #             ENTITY_NAME,
    #             name,
    #             OPERATION,
    #             operation,
    #             PAYLOAD_TYPE,
    #             payloadType);
    # }

    # public static void incrementWorkflowStartErrorCount(String workflowType, Throwable t) {
    #     incrementCount(
    #             WORKFLOW_START_ERROR,
    #             WORKFLOW_TYPE,
    #             workflowType,
    #             EXCEPTION,
    #             t.getClass().getSimpleName());
    # }

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
