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
workflow.register()
```

//Register the workflow with server
conductorWorkflow.Register(true)        //Overwrite the existing definition with the new one

### Execute Workflow

#### Using Workflow Executor to start previously registered workflow
```python
# TODO
```


Using struct instance as workflow input
```python
# TODO
```
### Workflow Management APIs
See [Docs](docs/executor.md) for APIs to start, pause, resume, terminate, search and get workflow execution status.

### More Examples
You can find more examples at the following GitHub repository:

https://github.com/conductor-sdk/conductor-examples/tree/main/python-samples
