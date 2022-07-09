<!-- markdownlint-disable -->

<a href="../src/conductor/client/workflow/task/event_task.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.workflow.task.event_task`






---

<a href="../src/conductor/client/workflow/task/event_task.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventTaskInterface`




<a href="../src/conductor/client/workflow/task/event_task.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(task_ref_name: str, event_prefix: str, event_suffix: str) → Self
```






---

#### <kbd>property</kbd> description





---

#### <kbd>property</kbd> input_parameters





---

#### <kbd>property</kbd> name





---

#### <kbd>property</kbd> optional





---

#### <kbd>property</kbd> task_reference_name





---

#### <kbd>property</kbd> task_type







---

<a href="../src/conductor/client/workflow/task/event_task.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_workflow_task`

```python
to_workflow_task() → WorkflowTask
```






---

<a href="../src/conductor/client/workflow/task/event_task.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SqsEventTask`




<a href="../src/conductor/client/workflow/task/event_task.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(task_ref_name: str, queue_name: str) → Self
```






---

#### <kbd>property</kbd> description





---

#### <kbd>property</kbd> input_parameters





---

#### <kbd>property</kbd> name





---

#### <kbd>property</kbd> optional





---

#### <kbd>property</kbd> task_reference_name





---

#### <kbd>property</kbd> task_type







---

<a href="../src/conductor/client/workflow/task/event_task.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_workflow_task`

```python
to_workflow_task() → WorkflowTask
```






---

<a href="../src/conductor/client/workflow/task/event_task.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ConductorEventTask`




<a href="../src/conductor/client/workflow/task/event_task.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(task_ref_name: str, event_name: str) → Self
```






---

#### <kbd>property</kbd> description





---

#### <kbd>property</kbd> input_parameters





---

#### <kbd>property</kbd> name





---

#### <kbd>property</kbd> optional





---

#### <kbd>property</kbd> task_reference_name





---

#### <kbd>property</kbd> task_type







---

<a href="../src/conductor/client/workflow/task/event_task.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_workflow_task`

```python
to_workflow_task() → WorkflowTask
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
