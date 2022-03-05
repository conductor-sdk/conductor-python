from conductor.client.configuration.configuration import Configuration
from conductor.client.telemetry.model.metric_documentation import MetricDocumentation
from conductor.client.telemetry.model.metric_label import MetricLabel
from conductor.client.telemetry.model.metric_name import MetricName
from prometheus_client import CollectorRegistry
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client.multiprocess import MultiProcessCollector
from typing import Dict, List
import os


class MetricsCollector:
    counters = {}
    registry = CollectorRegistry()

    def __init__(self):
        # TODO improve hard coded ENV
        os.environ["PROMETHEUS_MULTIPROC_DIR"] = Configuration.METRICS_PREFIX_DIR
        MultiProcessCollector(self.registry)

    def increment_task_poll_counter(self, task_type: str) -> None:
        self.__increment_counter(
            name=MetricName.TASK_POLL,
            documentation=MetricDocumentation.TASK_POLL,
            labels={
                MetricLabel.TASK_TYPE: task_type
            }
        )

    def increment_task_execution_queue_full_counter(self, task_type: str) -> None:
        self.__increment_counter(
            name=MetricName.TASK_EXECUTION_QUEUE_FULL,
            documentation=MetricDocumentation.TASK_EXECUTION_QUEUE_FULL,
            labels={
                MetricLabel.TASK_TYPE: task_type
            }
        )

    def increment_uncaught_exception_counter(self):
        self.__increment_counter(
            name=MetricName.THREAD_UNCAUGHT_EXCEPTION,
            documentation=MetricDocumentation.THREAD_UNCAUGHT_EXCEPTION,
            labels={}
        )

    def increment_task_poll_error_counter(self, task_type: str, exception: Exception) -> None:
        self.__increment_counter(
            name=MetricName.TASK_POLL_ERROR,
            documentation=MetricDocumentation.TASK_POLL_ERROR,
            labels={
                MetricLabel.TASK_TYPE: task_type,
                MetricLabel.EXCEPTION: str(exception)
            }
        )

    def increment_task_paused_counter(self, task_type: str) -> None:
        self.__increment_counter(
            name=MetricName.TASK_PAUSED,
            documentation=MetricDocumentation.TASK_PAUSED,
            labels={
                MetricLabel.TASK_TYPE: task_type
            }
        )

    def increment_task_execution_error_counter(self, task_type: str, exception: Exception) -> None:
        self.__increment_counter(
            name=MetricName.TASK_EXECUTE_ERROR,
            documentation=MetricDocumentation.TASK_EXECUTE_ERROR,
            labels={
                MetricLabel.TASK_TYPE: task_type,
                MetricLabel.EXCEPTION: str(exception)
            }
        )

    def increment_task_ack_failed_counter(self, task_type: str) -> None:
        self.__increment_counter(
            name=MetricName.TASK_ACK_FAILED,
            documentation=MetricDocumentation.TASK_ACK_FAILED,
            labels={
                MetricLabel.TASK_TYPE: task_type
            }
        )

    def increment_task_ack_error_counter(self, task_type: str, exception: Exception) -> None:
        self.__increment_counter(
            name=MetricName.TASK_ACK_ERROR,
            documentation=MetricDocumentation.TASK_ACK_ERROR,
            labels={
                MetricLabel.TASK_TYPE: task_type,
                MetricLabel.EXCEPTION: str(exception)
            }
        )

    # public static void recordTaskResultPayloadSize(String taskType, long payloadSize) {
    #     getGauge(TASK_RESULT_SIZE, TASK_TYPE, taskType).getAndSet(payloadSize);
    # }

    def increment_task_update_error_count(self, task_type: str, exception: Exception) -> None:
        self.__increment_counter(
            name=MetricName.TASK_UPDATE_ERROR,
            documentation=MetricDocumentation.TASK_UPDATE_ERROR,
            labels={
                MetricLabel.TASK_TYPE: task_type,
                MetricLabel.EXCEPTION: str(exception)
            }
        )

    # public static void recordWorkflowInputPayloadSize(
    #         String workflowType, String version, long payloadSize) {
    #     getGauge(WORKFLOW_INPUT_SIZE, WORKFLOW_TYPE, workflowType, WORKFLOW_VERSION, version)
    #             .getAndSet(payloadSize);
    # }

    def increment_external_payload_used_counter(self, entity_name: str, operation: str, payload_type: str) -> None:
        self.__increment_counter(
            name=MetricName.EXTERNAL_PAYLOAD_USED,
            documentation=MetricDocumentation.EXTERNAL_PAYLOAD_USED,
            labels={
                MetricLabel.ENTITY_NAME: entity_name,
                MetricLabel.OPERATION: operation,
                MetricLabel.PAYLOAD_TYPE: payload_type
            }
        )

    def increment_workflow_start_error_counter(self, workflow_type: str, exception: Exception) -> None:
        self.__increment_counter(
            name=MetricName.WORKFLOW_START_ERROR,
            documentation=MetricDocumentation.WORKFLOW_START_ERROR,
            labels={
                MetricLabel.WORKFLOW_TYPE: workflow_type,
                MetricLabel.EXCEPTION: str(exception)
            }
        )

    def __increment_counter(
        self,
        name: MetricName,
        documentation: MetricDocumentation,
        labels=Dict[MetricLabel, str]
    ) -> None:
        counter = self.__get_counter(
            name=name,
            documentation=documentation,
            labelnames=labels.keys()
        )
        counter.labels(*labels.values()).inc()

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
