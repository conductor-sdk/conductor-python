<!-- markdownlint-disable -->

<a href="../src/conductor/client/workflow/task/do_while_task.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.workflow.task.do_while_task`





---

<a href="../src/conductor/client/workflow/task/do_while_task.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_for_loop_condition`

```python
get_for_loop_condition(task_ref_name: str, iterations: int) → str
```






---

<a href="../src/conductor/client/workflow/task/do_while_task.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DoWhileTask`




<a href="../src/conductor/client/workflow/task/do_while_task.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    task_ref_name: str,
    termination_condition: str,
    tasks: List[TaskInterface]
) → Self
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

<a href="../src/conductor/client/workflow/task/do_while_task.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_workflow_task`

```python
to_workflow_task() → WorkflowTask
```






---

<a href="../src/conductor/client/workflow/task/do_while_task.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `LoopTask`




<a href="../src/conductor/client/workflow/task/do_while_task.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(task_ref_name: str, iterations: int, tasks: List[TaskInterface]) → Self
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

<a href="../src/conductor/client/workflow/task/do_while_task.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_workflow_task`

```python
to_workflow_task() → WorkflowTask
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
