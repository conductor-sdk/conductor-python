<!-- markdownlint-disable -->

<a href="../src/conductor/client/worker/worker_interface.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conductor.client.worker.worker_interface`






---

<a href="../src/conductor/client/worker/worker_interface.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `WorkerInterface`




<a href="../src/conductor/client/worker/worker_interface.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(task_definition_name: str)
```








---

<a href="../src/conductor/client/worker/worker_interface.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `execute`

```python
execute(task: Task) → TaskResult
```

Executes a task and returns the updated task. 

:param Task: (required) :return: TaskResult  If the task is not completed yet, return with the status as IN_PROGRESS. 

---

<a href="../src/conductor/client/worker/worker_interface.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_identity`

```python
get_identity() → str
```

Retrieve the hostname of the instance that the worker is running. 

:return: str 

---

<a href="../src/conductor/client/worker/worker_interface.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_polling_interval_in_seconds`

```python
get_polling_interval_in_seconds() → float
```

Retrieve interval in seconds at which the server should be polled for worker tasks. 

:return: float  Default: 100ms 

---

<a href="../src/conductor/client/worker/worker_interface.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_task_definition_name`

```python
get_task_definition_name() → str
```

Retrieve the name of the task definition the worker is currently working on. 

:return: TaskResult 

---

<a href="../src/conductor/client/worker/worker_interface.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_task_result_from_task`

```python
get_task_result_from_task(task: Task) → TaskResult
```

Retrieve the TaskResult object from given task. 

:param Task: (required) :return: TaskResult 




---
