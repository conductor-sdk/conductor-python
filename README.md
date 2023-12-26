# Conductor OSS Python SDK
Python SDK for working with https://github.com/conductor-oss/conductor

[Conductor](https://www.conductor-oss.org/) is an open source distributed, scalable and highly available 
orchestration platform that allows developers to build powerful distributed applications.
You can find the documentation for Conductor here: [Conductor Docs](https://orkes.io/content)

## ⭐ Conductor OSS
Show support for the Conductor OSS.  Please help spread the awareness by starring Conductor repo.

[![GitHub stars](https://img.shields.io/github/stars/conductor-oss/conductor.svg?style=social&label=Star&maxAge=)](https://GitHub.com/conductor-oss/conductor/)

## Content

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Install SDK](#install-sdk)
  - [Setup SDK](#setup-sdk)
- [Build a conductor workflow based application](#build-a-conductor-workflow-based-application)
- [Implement Worker](#implement-worker)
- [Create a workflow](#create-a-workflow)
  - [Execute workflow synchronously](#execute-workflow-synchronously)
  - [Execute workflow asynchronously](#execute-workflow-asynchronously)
- [Sending Signals to workflow](#sending-signals-to-workflow)
- [Testing your workflows](#testing-your-workflows)
- [Metrics support](#metrics-support)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Install SDK
Create a virtual environment to build your package
```shell
virtualenv conductor
source conductor/bin/activate
```

Get Conductor Python SDK
```shell
python3 -m pip install conductor-python
```
#### Setup SDK
SDK requires connecting to the Conductor server and optionally supplying with authentication parameters.

```python
from conductor.client.configuration.configuration import Configuration

configuration = Configuration(
    server_api_url='https://play.orkes.io/api',
    debug=False  # set to true for verbose logging
)
```
Configure the authentication settings if your Conductor server requires authentication.
```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings

configuration = Configuration(
    authentication_settings=AuthenticationSettings(
        key_id='key',
        key_secret='secret'
    )
)
```

See [Access Control](https://orkes.io/content/docs/getting-started/concepts/access-control) for guide to getting API keys

### Build a conductor workflow based application
Conductor lets you create workflows either in code or using the configuration in JSON that can be created form the code or from the UI.
Let's create a simple hello world application.

Create [greetings.py](examples/greetings.py) with a simple worker and a workflow function.

```python
from conductor.client.worker.worker_task import worker_task
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor


@worker_task(task_definition_name='save_order')
def greet(name: str) -> str:
    return f'Hello my friend {name}'


def greetings_workflow(name: str, workflow_exectuor: WorkflowExecutor) -> dict:
    workflow = ConductorWorkflow(name='hello', executor=workflow_exectuor)
    workflow >> greet(task_ref_name='greet_ref', name=workflow.input('name'))
    run = workflow.execute(workflow_input={'name': name})
    return run.output['result']

```

Let's add [greetings_main.py](examples/greetings_main.py) with the `main` method:
```python
import os
from multiprocessing import set_start_method

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from examples.greetings import greetings_workflow


def main():
    # Key and Secret are required for the servers with authentication enabled.
    key = os.getenv("KEY")
    secret = os.getenv("SECRET")
    url = os.getenv("CONDUCTOR_SERVER_URL")

    api_config = Configuration(authentication_settings=AuthenticationSettings(key_id=key, key_secret=secret),
                               server_api_url=url)

    workflow_executor = WorkflowExecutor(configuration=api_config)
    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
    )
    task_handler.start_processes()
    result = greetings_workflow('Orkes', workflow_executor)
    print(f'workflow result: {result}')
    task_handler.stop_processes()


if __name__ == '__main__':
    set_start_method('fork')
    main()

```

### Implement Worker
The workers can be implemented by writing a simple python function and annotating the function with the `@worker_task`
Conductor workers are services (similar to microservices) that follow [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single_responsibility_principle)

Workers can be hosted along with the workflow or running a distributed environment where a single workflow uses workers 
that are deployed and running in different machines/vms/containers.  Whether to keep all the workers in the same application or 
run them as distributed application is a design and architectural choice.  Conductor is well suited for both kind of scenarios.

A worker can take inputs which are primitives - `str`, `int`, `float`, `bool` etc. or can be complex data classes.

Here is an example worker that uses `dataclass` as part of the worker input.

```python
from conductor.client.worker.worker_task import worker_task
from dataclasses import dataclass

@dataclass
class OrderInfo:
    order_id: int
    sku: str
    quantity: int
    sku_price: float

    
@worker_task(task_definition_name='process_order')
def process_order(order_info: OrderInfo) -> str:
    return 'order_id_42'

```
#### Referencing a worker inside a workflow
A task inside a workflow represents a worker.  (sometimes both these words are used interchangeably).
Each task inside the workflow has two important identifiers:
1. name: Name of the task that represents the unique worker (e.g. task_definition_name in the above example)
2. reference name: Unique name _within_ the workflow for the task.  A single task can be added multiple times inside a workflow, reference name allows unique referencing of a specific instance of task in the workflow definition.

**Example when creating workflow in code**

```python
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
workflow = ConductorWorkflow()
workflow >> proces_order(task_ref_name='process_order_ref', order_info={})
```

**Example when creating workflow in JSON**
```json
{
  "name": "order_processing_wf",
  "description": "order_processing_wf",
  "version": 1,
  "tasks": [
    {
      "name": "process_order",
      "taskReferenceName": "process_order_ref",
      "type": "SIMPLE",
      "inputParameters": {
        "order_info": {}
      }
    }
  ],
  "timeoutPolicy": "TIME_OUT_WF",
  "timeoutSeconds": 60
}
```

### Create a workflow
#### Execute workflow synchronously
#### Execute workflow asynchronously
### Sending Signals to workflow
### Testing your workflows
### Metrics support



