<!-- markdownlint-disable -->

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>module</kbd> `conductor.client.workflow.executor.workflow_executor`






---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `WorkflowExecutor`




<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(configuration: Configuration) → Self
```








---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_by_correlation_ids`

```python
get_by_correlation_ids(
    workflow_name: str,
    include_closed: bool,
    include_tasks: bool,
    correlation_ids: List[str]
) → Dict[str, List[WorkflowDef]]
```

Lists workflows for the given correlation id list 

:param list[str] body: :param str name: :param bool include_closed: :param bool include_tasks: :return: dict(str, list[Workflow]) 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L210"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_task`

```python
get_task(task_id: str) → str
```

Get task by Id  

:param str task_id: :return: Task 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_workflow`

```python
get_workflow(workflow_id: str, include_tasks: bool) → Workflow
```

Gets the workflow by workflow id 

:param str workflow_id: :param bool include_tasks: :return: Workflow 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_workflow_status`

```python
get_workflow_status(
    workflow_id: str,
    include_output: bool,
    include_variables: bool
) → WorkflowStatus
```

Gets the workflow by workflow id 

:param str workflow_id: :param bool include_output: :param bool include_variables: :return: WorkflowStatus 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pause`

```python
pause(workflow_id: str) → None
```

Pauses the workflow 

:param str workflow_id: :return: None 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `register_workflow`

```python
register_workflow(workflow: WorkflowDef, overwrite: bool) → object
```

Create a new workflow definition 

:param WorkflowDef body: :param bool overwrite: :return: object 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L155"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `rerun`

```python
rerun(rerun_workflow_request: RerunWorkflowRequest, workflow_id: str) → str
```

Reruns the workflow from a specific task 

:param RerunWorkflowRequest body: :param str workflow_id: :return: str 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `restart`

```python
restart(workflow_id: str, use_latest_definitions: bool) → None
```

Restarts a completed workflow 

:param str workflow_id: :param bool use_latest_definitions: :return: None 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `resume`

```python
resume(workflow_id: str) → None
```

Resumes the workflow 

:param str workflow_id: :return: None 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retry`

```python
retry(workflow_id: str, resume_subworkflow_tasks: bool) → None
```

Retries the last failed task   

:param str workflow_id: :param bool resume_subworkflow_tasks: :return: None 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search`

```python
search(
    start: int,
    size: int,
    query: str,
    free_text: str
) → ScrollableSearchResultWorkflowSummary
```

Search for workflows based on payload and other parameters 

:param async_req bool :param str query_id: :param int start: :param int size: :param str sort: :param str free_text: :param str query: :param bool skip_cache: :return: ScrollableSearchResultWorkflowSummary 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L167"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `skip_task_from_workflow`

```python
skip_task_from_workflow(
    workflow_id: str,
    task_reference_name: str,
    skip_task_request: SkipTaskRequest
) → None
```

Skips a given task from a current running workflow 

:param str workflow_id: :param str task_reference_name: :param SkipTaskRequest body: :return: None 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `start_workflow`

```python
start_workflow(start_workflow_request: StartWorkflowRequest) → str
```

Start a new workflow with StartWorkflowRequest, which allows task to be executed in a domain  

:param StartWorkflowRequest body: :return: str 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `terminate`

```python
terminate(workflow_id: str, reason: str) → None
```

Terminate workflow execution 

:param str workflow_id: :param str reason: :return: None 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L181"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_task`

```python
update_task(
    task_id: str,
    workflow_id: str,
    task_output: Dict[str, Any],
    status: str
) → str
```

Update a task 

:param TaskResult body: :return: str 

---

<a href="../src/conductor/client/workflow/executor/workflow_executor.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_task_by_ref_name`

```python
update_task_by_ref_name(
    task_output: Dict[str, Any],
    workflow_id: str,
    task_reference_name: str,
    status: str
) → str
```

Update a task By Ref Name   

:param dict(str, object) body: :param str workflow_id: :param str task_ref_name: :param str status: :return: str 




---
