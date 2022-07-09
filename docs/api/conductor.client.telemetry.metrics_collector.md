<!-- markdownlint-disable -->

<a href="../src/conductor/client/telemetry/metrics_collector.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.telemetry.metrics_collector`






---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MetricsCollector`




<a href="../src/conductor/client/telemetry/metrics_collector.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(settings: MetricsSettings)
```








---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_external_payload_used`

```python
increment_external_payload_used(
    entity_name: str,
    operation: str,
    payload_type: str
) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_task_ack_error`

```python
increment_task_ack_error(task_type: str, exception: Exception) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_task_ack_failed`

```python
increment_task_ack_failed(task_type: str) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_task_execution_error`

```python
increment_task_execution_error(task_type: str, exception: Exception) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_task_execution_queue_full`

```python
increment_task_execution_queue_full(task_type: str) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_task_paused`

```python
increment_task_paused(task_type: str) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_task_poll`

```python
increment_task_poll(task_type: str) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_task_poll_error`

```python
increment_task_poll_error(task_type: str, exception: Exception) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_task_update_error`

```python
increment_task_update_error(task_type: str, exception: Exception) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_uncaught_exception`

```python
increment_uncaught_exception()
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L146"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `increment_workflow_start_error`

```python
increment_workflow_start_error(workflow_type: str, exception: Exception) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `provide_metrics`

```python
provide_metrics(settings: MetricsSettings) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `record_task_execute_time`

```python
record_task_execute_time(task_type: str, time_spent: float) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L177"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `record_task_poll_time`

```python
record_task_poll_time(task_type: str, time_spent: float) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L167"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `record_task_result_payload_size`

```python
record_task_result_payload_size(task_type: str, payload_size: int) → None
```





---

<a href="../src/conductor/client/telemetry/metrics_collector.py#L156"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `record_workflow_input_payload_size`

```python
record_workflow_input_payload_size(
    workflow_type: str,
    version: str,
    payload_size: int
) → None
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
