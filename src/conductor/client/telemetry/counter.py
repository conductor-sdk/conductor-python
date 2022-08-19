from conductor.client.telemetry.model.metric_documentation import MetricDocumentation
from conductor.client.telemetry.model.metric_label import MetricLabel
from conductor.client.telemetry.model.metric_name import MetricName
from prometheus_client import Counter
from typing import Dict, List
import logging

_logger = logging.getLogger(__name__)

_counters = {}


def increment_task_poll(task_type: str) -> None:
    _increment_counter(
        name=MetricName.TASK_POLL,
        documentation=MetricDocumentation.TASK_POLL,
        labels={
            MetricLabel.TASK_TYPE: task_type
        }
    )


def increment_task_execution_queue_full(task_type: str) -> None:
    _increment_counter(
        name=MetricName.TASK_EXECUTION_QUEUE_FULL,
        documentation=MetricDocumentation.TASK_EXECUTION_QUEUE_FULL,
        labels={
            MetricLabel.TASK_TYPE: task_type
        }
    )


def increment_uncaught_exception():
    _increment_counter(
        name=MetricName.THREAD_UNCAUGHT_EXCEPTION,
        documentation=MetricDocumentation.THREAD_UNCAUGHT_EXCEPTION,
        labels={}
    )


def increment_task_poll_error(task_type: str, exception: Exception) -> None:
    _increment_counter(
        name=MetricName.TASK_POLL_ERROR,
        documentation=MetricDocumentation.TASK_POLL_ERROR,
        labels={
            MetricLabel.TASK_TYPE: task_type,
            MetricLabel.EXCEPTION: str(exception)
        }
    )


def increment_task_paused(task_type: str) -> None:
    _increment_counter(
        name=MetricName.TASK_PAUSED,
        documentation=MetricDocumentation.TASK_PAUSED,
        labels={
            MetricLabel.TASK_TYPE: task_type
        }
    )


def increment_task_execution_error(task_type: str, exception: Exception) -> None:
    _increment_counter(
        name=MetricName.TASK_EXECUTE_ERROR,
        documentation=MetricDocumentation.TASK_EXECUTE_ERROR,
        labels={
            MetricLabel.TASK_TYPE: task_type,
            MetricLabel.EXCEPTION: str(exception)
        }
    )


def increment_task_ack_failed(task_type: str) -> None:
    _increment_counter(
        name=MetricName.TASK_ACK_FAILED,
        documentation=MetricDocumentation.TASK_ACK_FAILED,
        labels={
            MetricLabel.TASK_TYPE: task_type
        }
    )


def increment_task_ack_error(task_type: str, exception: Exception) -> None:
    _increment_counter(
        name=MetricName.TASK_ACK_ERROR,
        documentation=MetricDocumentation.TASK_ACK_ERROR,
        labels={
            MetricLabel.TASK_TYPE: task_type,
            MetricLabel.EXCEPTION: str(exception)
        }
    )


def increment_task_update_error(task_type: str, exception: Exception) -> None:
    _increment_counter(
        name=MetricName.TASK_UPDATE_ERROR,
        documentation=MetricDocumentation.TASK_UPDATE_ERROR,
        labels={
            MetricLabel.TASK_TYPE: task_type,
            MetricLabel.EXCEPTION: str(exception)
        }
    )


def increment_external_payload_used(entity_name: str, operation: str, payload_type: str) -> None:
    _increment_counter(
        name=MetricName.EXTERNAL_PAYLOAD_USED,
        documentation=MetricDocumentation.EXTERNAL_PAYLOAD_USED,
        labels={
            MetricLabel.ENTITY_NAME: entity_name,
            MetricLabel.OPERATION: operation,
            MetricLabel.PAYLOAD_TYPE: payload_type
        }
    )


def increment_workflow_start_error(workflow_type: str, exception: Exception) -> None:
    _increment_counter(
        name=MetricName.WORKFLOW_START_ERROR,
        documentation=MetricDocumentation.WORKFLOW_START_ERROR,
        labels={
            MetricLabel.WORKFLOW_TYPE: workflow_type,
            MetricLabel.EXCEPTION: str(exception)
        }
    )


def _increment_counter(
    name: MetricName,
    documentation: MetricDocumentation,
    labels: Dict[MetricLabel, str]
) -> None:
    counter = _get_counter(
        name=name,
        documentation=documentation,
        labelnames=labels.keys()
    )
    counter.labels(*labels.values()).inc()


def _get_counter(
    name: MetricName,
    documentation: MetricDocumentation,
    labelnames: List[MetricLabel]
) -> Counter:
    if name not in _counters:
        _counters[name] = _generate_counter(
            name, documentation, labelnames
        )
    return _counters[name]


def _generate_counter(
    name: MetricName,
    documentation: MetricDocumentation,
    labelnames: List[MetricLabel]
) -> Counter:
    return Counter(
        name=name,
        documentation=documentation,
        labelnames=labelnames,
    )
