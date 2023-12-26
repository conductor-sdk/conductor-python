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
  - [Step 1: Create a Workflow](#step-1-create-a-workflow)
  - [Step 2: Write Worker](#step-2-write-worker)
  - [Step 3: Write _your_ application](#step-3-write-_your_-application)
- [Implementing Workers](#implementing-workers)
  - [Referencing a worker inside a workflow](#referencing-a-worker-inside-a-workflow)
- [Executing Workflows](#executing-workflows)
  - [Execute workflow synchronously](#execute-workflow-synchronously)
  - [Execute workflow asynchronously](#execute-workflow-asynchronously)
- [Sending Signals to workflow](#sending-signals-to-workflow)
- [Testing your workflows](#testing-your-workflows)
- [Metrics support](#metrics-support)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Install SDK
Create a virtual environment to build your package
```shell
virtualenv conductor
source conductor/bin/activate
```

Get Conductor Python SDK
```shell
python3 -m pip install conductor-python
```
### Setup SDK
SDK requires connecting to the Conductor server and optionally supplying with authentication parameters.

```python
from conductor.client.configuration.configuration import Configuration

configuration = Configuration(server_api_url='https://play.orkes.io/api')
```
Configure the authentication settings _if your Conductor server requires authentication_.
See [Access Control](https://orkes.io/content/docs/getting-started/concepts/access-control) for guide to getting API keys
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

## Start Conductor Server
```shell
docker run --init -p 8080:8080 -p 1234:5000 conductoross/conductor-standalone:3.15.0
```
After starting the server navigate to http://localhost:1234 to ensure the server has started successfully.

## Build a conductor workflow based application
Conductor lets you create workflows either in code or using the configuration in JSON that can be created form the code or from the UI.
We will explore both the options here.

An application using Conductor uses the following:
1. **Workflow**: Describes the application's state and how functions are wired.  Workflow is what gives your application's code durability and full-blown visualization in the Conductor UI.
2. **Worker**: Stateless components.  Workers can be exposed as HTTP endpoints (aka Microservices) or can be simple task workers implemented using lightweight Conductor SDK in the framework and language of your choice.

Note: A single workflow application can have workers written in different languages.

### Step 1: Create a Workflow

**Use JSON to create workflows**

Create workflow.json with the following:
```json
{
  "name": "hello",
  "description": "hello workflow",
  "version": 1,
  "tasks": [
    {
      "name": "greet",
      "taskReferenceName": "greet_ref",
      "type": "SIMPLE",
      "inputParameters": {
        "name": "${workflow.input.name}"
      }
    }
  ],
  "timeoutPolicy": "TIME_OUT_WF",
  "timeoutSeconds": 60
}
```
Now, register this workflow with the server:
```shell
curl -X POST -H "Content-Type:application/json" http://localhost:8080/api/metadata/workflow -d @workflow.json
```

**Use Code to create workflows**

Create greetings_workflow.py with the following:
```python
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from examples.greetings import greet

def greetings_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    workflow = ConductorWorkflow(name='hello', executor=workflow_executor)
    workflow >> greet(task_ref_name='greet_ref', name=workflow.input('name'))
    return workflow

```

### Step 2: Write Worker

Create [greetings.py](examples/greetings.py) with a simple worker and a workflow function.

```python
from conductor.client.worker.worker_task import worker_task


@worker_task(task_definition_name='greet')
def greet(name: str) -> str:
    return f'Hello my friend {name}'

```

### Step 3: Write _your_ application

Let's add [greetings_main.py](examples/greetings_main.py) with the `main` method:
```python
from multiprocessing import set_start_method

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import WorkflowRun
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from examples.greetings_workflow import greetings_workflow

def greetings_workflow_run(name: str, workflow_executor: WorkflowExecutor) -> WorkflowRun:
    return workflow_executor.execute(name='hello', version=1, workflow_input={'name': name})


def main():
    # points to http://localhost:8080/api by default
    api_config = Configuration()

    workflow_executor = WorkflowExecutor(configuration=api_config)
    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
        import_modules=['examples.greetings']
    )
    task_handler.start_processes()

    # ------------------------------------------------------------------------------------
    # Important: When defining the workflow using code, un-comment the following two lines
    # ------------------------------------------------------------------------------------
    # workflow = greetings_workflow(workflow_executor=workflow_executor)
    # workflow.register(True)
  
    result = greetings_workflow_run('Orkes', workflow_executor)
    print(f'workflow result: {result.output["result"]}')
    task_handler.stop_processes()


if __name__ == '__main__':
    set_start_method('fork')
    main()
```

## Implementing Workers
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
### Referencing a worker inside a workflow
A task inside a workflow represents a worker.  (sometimes both these words are used interchangeably).
Each task inside the workflow has two important identifiers:
1. name: Name of the task that represents the unique worker (e.g. task_definition_name in the above example)
2. reference name: Unique name _within_ the workflow for the task.  A single task can be added multiple times inside a workflow, reference name allows unique referencing of a specific instance of task in the workflow definition.

**Example when creating workflow in code**

```python
from conductor.client.workflow.conductor_workflow import ConductorWorkflow

# ---------- task ↓ ------------->task reference name ↓ ---- task inputs ↓ ---
workflow >> proces_order(task_ref_name='process_order_ref', order_info=OrderInfo())
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

## Executing Workflows
[WorkflowClient](src/conductor/client/workflow_client.py) interface provides all the APIs required to work with workflow executions.
```python
api_config = Configuration()
workflow_client = 
```
### Execute workflow synchronously
### Execute workflow asynchronously
### Execute dynamic workflows using Code

## Sending Signals to workflow
## Testing your workflows
## Metrics support



