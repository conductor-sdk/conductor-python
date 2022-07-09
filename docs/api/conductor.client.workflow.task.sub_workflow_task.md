<!-- markdownlint-disable -->

<a href="../src/conductor/client/workflow/task/sub_workflow_task.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.workflow.task.sub_workflow_task`






---

<a href="../src/conductor/client/workflow/task/sub_workflow_task.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SubWorkflowTask`




<a href="../src/conductor/client/workflow/task/sub_workflow_task.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    task_ref_name: str,
    workflow_name: str,
    version: int = None,
    task_to_domain_map: Dict[str, str] = None
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

<a href="../src/conductor/client/workflow/task/sub_workflow_task.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_workflow_task`

```python
to_workflow_task() → WorkflowTask
```






---

<a href="../src/conductor/client/workflow/task/sub_workflow_task.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `InlineSubWorkflowTask`




<a href="../src/conductor/client/workflow/task/sub_workflow_task.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(task_ref_name: str, workflow: ConductorWorkflow) → Self
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

<a href="../src/conductor/client/workflow/task/sub_workflow_task.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_workflow_task`

```python
to_workflow_task() → WorkflowTask
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
