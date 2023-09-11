# Authoring Workflows

## A simple two-step guide

### Define workflow

In order to define a workflow, you must provide a `WorkflowExecutor`, which requires a `Configuration` object with the Conductor Server info. Here's an example on how to do that:

```python
configuration = Configuration()
workflow_executor = WorkflowExecutor(configuration)
workflow = ConductorWorkflow(
    executor=workflow_executor,
    name='python_workflow_example_from_code',
    description='Python workflow example from code'
)
```

If your setup requires special authentication or self-signed certs it might be worth providing your own http connection object as follows: 


```python
import requests
from custom_auth import CustomAdapter  # your custom auth adapter

session = requests.Session()
session.mount("https://", CustomAdapter())
configuration = Configuration()
configuration.http_connection = session

workflow_executor = WorkflowExecutor(configuration)
workflow = ConductorWorkflow(
    executor=workflow_executor,
    name='python_workflow_example_from_code',
    description='Python workflow example from code'
)
```

After creating an instance of a `ConductorWorkflow`, you can start adding tasks to it. There are two possible ways to do that:
* method: `add`
* operator: `>>`

```python
simple_task_1 = SimpleTask(
    task_def_name='python_simple_task_from_code_1',
    task_reference_name='python_simple_task_from_code_1'
)
workflow.add(simple_task_1)

simple_task_2 = SimpleTask(
    task_def_name='python_simple_task_from_code_2',
    task_reference_name='python_simple_task_from_code_2'
)
workflow >> simple_task_2
```

You should be able to register your workflow at the Conductor Server:

```python
workflow.register(true)
```

### Workflow Executor 

#### Using Workflow Executor to start previously registered workflow
```python
workflow_id = workflow_executor.start_workflow(
    start_workflow_request=StartWorkflowRequest(
        name=workflow.name
    )
)
```


### Workflow Management APIs
See [Docs](./../api/conductor.client.workflow.executor.workflow_executor.md) for APIs to start, pause, resume, terminate, search and get workflow execution status.
