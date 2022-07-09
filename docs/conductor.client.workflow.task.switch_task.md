<!-- markdownlint-disable -->

<a href="../src/conductor/client/workflow/task/switch_task.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.workflow.task.switch_task`






---

<a href="../src/conductor/client/workflow/task/switch_task.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EvaluatorType`
An enumeration. 





---

<a href="../src/conductor/client/workflow/task/switch_task.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SwitchTask`




<a href="../src/conductor/client/workflow/task/switch_task.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    task_ref_name: str,
    case_expression: str,
    use_javascript: bool = False
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

<a href="../src/conductor/client/workflow/task/switch_task.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `default_case`

```python
default_case(tasks: List[TaskInterface]) → Self
```





---

<a href="../src/conductor/client/workflow/task/switch_task.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `switch_case`

```python
switch_case(case_name: str, tasks: List[TaskInterface]) → Self
```





---

<a href="../src/conductor/client/workflow/task/switch_task.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_workflow_task`

```python
to_workflow_task() → WorkflowTask
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
