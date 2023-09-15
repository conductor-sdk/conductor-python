# Authoring Workflows

### Register Workflow Definition

In order to define a workflow, you must provide a `OrkesMetadataClient` and a `WorkflowExecutor`, which requires a `Configuration` object with the Conductor Server info. Here's an example on how to do that:

```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.orkes.orkes_metadata_client import OrkesMetadataClient
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.simple_task import SimpleTask

configuration = Configuration(
    server_api_url=SERVER_API_URL,
    debug=False,
    authentication_settings=AuthenticationSettings(
        key_id=KEY_ID,
        key_secret=KEY_SECRET
    ),
)
metadata_client = OrkesMetadataClient(configuration)
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
You can add input parameters to your workflow:

```python
workflow.input_parameters(["a", "b"])
```

You should be able to register your workflow at the Conductor Server:

```python
workflowDef = workflow.to_workflow_def()
metadata_client.registerWorkflowDef(workflowDef, True)
```

### Update Workflow Definition

You should be able to unregister your workflow by passing name and version:

```python
workflow >> SimpleTask("simple_task", "simple_task_ref_2")
updatedWorkflowDef = workflow.to_workflow_def()
metadata_client.updateWorkflowDef(updatedWorkflowDef, True)
```

### Unregister Workflow Definition

You should be able to unregister your workflow by passing name and version:

```python
metadata_client.unregisterWorkflowDef('python_workflow_example_from_code', 1)
```