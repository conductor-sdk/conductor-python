<!-- markdownlint-disable -->

<a href="../src/conductor/client/workflow/task/http_task.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.workflow.task.http_task`






---

<a href="../src/conductor/client/workflow/task/http_task.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `HttpMethod`
An enumeration. 





---

<a href="../src/conductor/client/workflow/task/http_task.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `HttpInput`




<a href="../src/conductor/client/workflow/task/http_task.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    method: HttpMethod = <HttpMethod.GET: 'GET'>,
    uri: str = None,
    headers: Dict[str, List[str]] = None,
    accept: str = None,
    content_type: str = None,
    connection_time_out: int = None,
    read_timeout: int = None,
    body: Any = None
) → Self
```









---

<a href="../src/conductor/client/workflow/task/http_task.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `HttpTask`




<a href="../src/conductor/client/workflow/task/http_task.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(task_ref_name: str, http_input: HttpInput) → Self
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

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
