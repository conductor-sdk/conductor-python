from conductor.client.telemetry.model.metric_documentation import MetricDocumentation
from conductor.client.telemetry.model.metric_label import MetricLabel
from conductor.client.telemetry.model.metric_name import MetricName
from prometheus_client import Gauge
from typing import Any, Dict, List
import logging

_logger = logging.getLogger(__name__)
_gauges = {}


def record_workflow_input_payload_size(workflow_type: str, version: str, payload_size: int) -> None:
    _record_gauge(
        name=MetricName.WORKFLOW_INPUT_SIZE,
        documentation=MetricDocumentation.WORKFLOW_INPUT_SIZE,
        labels={
            MetricLabel.WORKFLOW_TYPE: workflow_type,
            MetricLabel.WORKFLOW_VERSION: version
        },
        value=payload_size
    )


def record_task_result_payload_size(task_type: str, payload_size: int) -> None:
    _record_gauge(
        name=MetricName.TASK_RESULT_SIZE,
        documentation=MetricDocumentation.TASK_RESULT_SIZE,
        labels={
            MetricLabel.TASK_TYPE: task_type
        },
        value=payload_size
    )


def record_task_poll_time(task_type: str, time_spent: float) -> None:
    _record_gauge(
        name=MetricName.TASK_POLL_TIME,
        documentation=MetricDocumentation.TASK_POLL_TIME,
        labels={
            MetricLabel.TASK_TYPE: task_type
        },
        value=time_spent
    )


def record_task_execute_time(task_type: str, time_spent: float) -> None:
    _record_gauge(
        name=MetricName.TASK_EXECUTE_TIME,
        documentation=MetricDocumentation.TASK_EXECUTE_TIME,
        labels={
            MetricLabel.TASK_TYPE: task_type
        },
        value=time_spent
    )


def _record_gauge(
    name: MetricName,
    documentation: MetricDocumentation,
    labels: Dict[MetricLabel, str],
    value: Any
) -> None:
    gauge = _get_gauge(
        name=name,
        documentation=documentation,
        labelnames=labels.keys()
    )
    gauge.labels(*labels.values()).set(value)


def _get_gauge(
    name: MetricName,
    documentation: MetricDocumentation,
    labelnames: List[MetricLabel]
) -> Gauge:
    if name not in _gauges:
        _gauges[name] = _generate_gauge(
            name, documentation, labelnames
        )
    return _gauges[name]


def _generate_gauge(
    name: MetricName,
    documentation: MetricDocumentation,
    labelnames: List[MetricLabel]
) -> Gauge:
    return Gauge(
        name=name,
        documentation=documentation,
        labelnames=labelnames,
    )
