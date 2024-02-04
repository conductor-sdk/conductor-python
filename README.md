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
  - [Get Conductor Python SDK](#get-conductor-python-sdk)
  - [Setup SDK](#setup-sdk)
- [Start Conductor Server](#start-conductor-server)
- [Simple Hello World Application using Conductor](#simple-hello-world-application-using-conductor)
  - [Step 1: Create a Workflow](#step-1-create-a-workflow)
  - [Step 2: Write Worker](#step-2-write-worker)
  - [Step 3: Write _your_ application](#step-3-write-_your_-application)
- [Using Conductor in your application](#using-conductor-in-your-application)
  - [Create and Run Conductor Workers](#create-and-run-conductor-workers)
  - [Create Conductor Workflows](#create-conductor-workflows)
  - [Using Conductor in your Application](#using-conductor-in-your-application)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Install SDK
Create a virtual environment to build your package
```shell
virtualenv conductor
source conductor/bin/activate
```

### Get Conductor Python SDK

SDK needs Python 3.9+.

```shell
python3 -m pip install conductor-python
```
### Setup SDK

Point the SDK to the Conductor Server API endpoint
```shell
export CONDUCTOR_SERVER_URL=http://localhost:8080/api
```
(Optionally) If you are using a Conductor server that requires authentication

[How to obtain the key and secret from the conductor server
](https://orkes.io/content/docs/getting-started/concepts/access-control)


```shell
export CONDUCTOR_AUTH_KEY=your_key
export CONDUCTOR_AUTH_SECRET=your_key_secret
```

## Start Conductor Server
```shell
docker run --init -p 8080:8080 -p 1234:5000 conductoross/conductor-standalone:3.15.0
```
After starting the server navigate to http://localhost:1234 to ensure the server has started successfully.

## Simple Hello World Application using Conductor
In this section, we will create a simple "Hello World" application that uses Conductor. 

### Step 1: Create a Workflow

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

**(alternatively) Use JSON to create workflows**

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
curl -X POST -H "Content-Type:application/json" \
http://localhost:8080/api/metadata/workflow -d @workflow.json
```

### Step 2: Write Worker

Create [greetings.py](examples/greetings.py) with a simple worker and a workflow function.

> [!note]
> A single workflow application can have workers written in different languages.

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


def register_workflow(workflow_executor: WorkflowExecutor):
    workflow = greetings_workflow(workflow_executor=workflow_executor)
    workflow.register(True)

def main():
  
    # points to http://localhost:8080/api by default
    api_config = Configuration()

    workflow_executor = WorkflowExecutor(configuration=api_config)

    # Needs to be done only when registering a workflow one-time
    register_workflow(workflow_executor)

    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
        import_modules=['examples.greetings']
    )
    task_handler.start_processes()

    result = greetings_workflow_run('Orkes', workflow_executor)
    print(f'workflow result: {result.output["result"]}')
    task_handler.stop_processes()


if __name__ == '__main__':
    main()
```

> [!NOTE]
> That's it - you just created your first distributed python app!
> 

## Using Conductor in your application
There are three main ways you will use Conductor when building durable, resilient, distributed applications.
1. Write service workers that implements business logic to accomplish a specific goal - such as initiate payment transfer, get user information from database etc. 
2. Create Conductor workflows that implements application state - A typical workflow implements SAGA pattern
3. Use Conductor SDK and APIs to manage workflows from your application.

In this guide, we will dive deeper into each of these topic.

### [Create and Run Conductor Workers](WORKERS.md)
### [Create Conductor Workflows](WORKFLOW.md)
### [Using Conductor in your Application](CONDUCTOR_APP.md)





