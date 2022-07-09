<!-- markdownlint-disable -->

<a href="../src/conductor/client/workflow/task/task.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.workflow.task.task`





---

<a href="../src/conductor/client/workflow/task/task.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_task_interface_list_as_workflow_task_list`

```python
get_task_interface_list_as_workflow_task_list(*tasks: Self) → List[WorkflowTask]
```






---

<a href="../src/conductor/client/workflow/task/task.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TaskInterface`




<a href="../src/conductor/client/workflow/task/task.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    task_reference_name: str,
    task_type: TaskType,
    task_name: str = None,
    description: str = None,
    optional: bool = None,
    input_parameters: Dict[str, Any] = None
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

<a href="../src/conductor/client/workflow/task/task.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `input`

```python
input(key: str, value: Any) → Self
```





---

<a href="../src/conductor/client/workflow/task/task.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `output_ref`

```python
output_ref(path: str) → str
```





---

<a href="../src/conductor/client/workflow/task/task.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_workflow_task`

```python
to_workflow_task() → WorkflowTask
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
