<!-- markdownlint-disable -->

<a href="../src/conductor/client/workflow/conductor_workflow.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.workflow.conductor_workflow`






---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ConductorWorkflow`




<a href="../src/conductor/client/workflow/conductor_workflow.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    executor: WorkflowExecutor,
    name: str,
    version: int = None,
    description: str = None
) → Self
```






---

#### <kbd>property</kbd> description





---

#### <kbd>property</kbd> name





---

#### <kbd>property</kbd> version







---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add`

```python
add(task: TaskInterface) → Self
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `failure_workflow`

```python
failure_workflow(failure_workflow: str) → Self
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `input_parameters`

```python
input_parameters(input_parameters: List[str]) → Self
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L113"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `input_template`

```python
input_template(input_template: Dict[str, Any]) → Self
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `output_parameters`

```python
output_parameters(output_parameters: Dict[str, Any]) → Self
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `owner_email`

```python
owner_email(owner_email: str) → Self
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L151"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `register`

```python
register(overwrite: bool)
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `restartable`

```python
restartable(restartable: bool) → Self
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `timeout_policy`

```python
timeout_policy(timeout_policy: TimeoutPolicy) → Self
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `timeout_seconds`

```python
timeout_seconds(timeout_seconds: int) → Self
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_workflow_def`

```python
to_workflow_def() → WorkflowDef
```





---

<a href="../src/conductor/client/workflow/conductor_workflow.py#L127"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `variables`

```python
variables(variables: Dict[str, Any]) → Self
```








---
