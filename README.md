# Conductor OSS Python SDK

Python SDK for working with https://github.com/conductor-oss/conductor

[Conductor](https://www.conductor-oss.org/) is the leading open-source orchestration platform allowing developers to build highly scalable distributed applications.

Check out the [official documentation for Conductor](https://orkes.io/content).

## ⭐ Conductor OSS

Show support for the Conductor OSS.  Please help spread the awareness by starring Conductor repo.

[![GitHub stars](https://img.shields.io/github/stars/conductor-oss/conductor.svg?style=social&label=Star&maxAge=)](https://GitHub.com/conductor-oss/conductor/)

## Content

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Install SDK](#install-sdk)
  - [Get Conductor Python SDK](#get-conductor-python-sdk)
- [Simple Hello World Application Using Conductor](#simple-hello-world-application-using-conductor)
  - [Step 1: Create Workflow](#step-1-create-workflow)
    - [Use Code to Create Workflows](#use-code-to-create-workflows)
    - [(Alternatively) Use JSON to Create Workflows](#alternatively-use-json-to-create-workflows)
  - [Step 2: Write Worker](#step-2-write-worker)
  - [Step 3: Write _Your_ Application](#step-3-write-_your_-application)
- [Running Workflow Locally](#running-workflow-locally)
  - [Setup SDK](#setup-sdk)
  - [Start Conductor Server](#start-conductor-server)
- [Running Workflow in Orkes Conductor](#running-workflow-in-orkes-conductor)
- [How does the app work?](#how-does-the-app-work)
- [Using Conductor in Your Application](#using-conductor-in-your-application)
  - [Create and Run Conductor Workers](#create-and-run-conductor-workers)
  - [Create Conductor Workflows](#create-conductor-workflows)
  - [Using Conductor in your Application](#using-conductor-in-your-application)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Install SDK

Create a virtual environment to build your package.

```shell
virtualenv conductor
source conductor/bin/activate
```

### Get Conductor Python SDK

SDK needs Python 3.9+.

```shell
python3 -m pip install conductor-python
```

## Simple Hello World Application Using Conductor

In this section, we will create a simple "Hello World" application that uses Conductor.

### Step 1: Create Workflow

#### Use Code to Create Workflows

Create [greetings_workflow.py](examples/greetings_workflow.py) with the following:

```python
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from greetings import greet

def greetings_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    name = 'hello'
    workflow = ConductorWorkflow(name=name, executor=workflow_executor)
    workflow.version = 1
    workflow >> greet(task_ref_name='greet_ref', name=workflow.input('name'))
    return workflow


```

#### (Alternatively) Use JSON to Create Workflows

Create `workflow.json` with the following:

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

Create [greetings.py](examples/greetings.py) with a simple worker and workflow function.

> [!note]
> A single workflow application can have workers written in different languages.

```python
from conductor.client.worker.worker_task import worker_task


@worker_task(task_definition_name='greet')
def greet(name: str) -> str:
    return f'Hello my friend {name}'

```

### Step 3: Write _Your_ Application

Let's add [greetings_main.py](examples/greetings_main.py) with the `main` method:

```python
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from greetings_workflow import greetings_workflow


def register_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    workflow = greetings_workflow(workflow_executor=workflow_executor)
    workflow.register(True)
    return workflow


def main():
    # points to http://localhost:8080/api by default
    api_config = Configuration()

    workflow_executor = WorkflowExecutor(configuration=api_config)

    # Needs to be done only when registering a workflow one-time
    workflow = register_workflow(workflow_executor)

    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()

    workflow_run = workflow_executor.execute(name=workflow.name, version=workflow.version,
                                             workflow_input={'name': 'Orkes'})

    print(f'\nworkflow result: {workflow_run.output["result"]}\n')
    print(f'see the workflow execution here: {api_config.ui_host}/execution/{workflow_run.workflow_id}\n')
    task_handler.stop_processes()


if __name__ == '__main__':
    main()
```
## Running Workflow Locally

### Setup SDK

Point the SDK to the Conductor Server API endpoint. Now, let's test the app locally:

```shell
export CONDUCTOR_SERVER_URL=http://localhost:8080/api
```
### Start Conductor Server
```shell
docker run --init -p 8080:8080 -p 5000:5000 conductoross/conductor-standalone:3.15.0
```
After starting the server, navigate to http://localhost:5000 to ensure the server has started successfully. 

```
python greetings_workflow.py
```

Now, the workflow is executed, and the execution can be viewed from the Conductor UI (http://localhost:5000).

Navigate to the **Executions** tab to view the workflow execution.

<img width="1434" alt="Screenshot 2024-03-18 at 12 30 07" src="https://github.com/Srividhya-S-Subramanian/conductor-python-v1/assets/163816773/11e829b6-d46a-4b47-b2cf-0bf524a6ebdc">

Open the Workbench tab and try running the 'hello' workflow. You will notice that the workflow execution fails. This is because task_handler.stop_processes() [greetings_main.py], stops all the workers. So, workers are not available to execute the tasks.

Now, let's update `greetings_main.py`

```python
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from greetings_workflow import greetings_workflow


def register_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    workflow = greetings_workflow(workflow_executor=workflow_executor)
    workflow.register(True)
    return workflow


def main():
    # points to http://localhost:8080/api by default
    api_config = Configuration()

    workflow_executor = WorkflowExecutor(configuration=api_config)

    # Needs to be done only when registering a workflow one-time
    workflow = register_workflow(workflow_executor)

    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()

    #workflow_run = workflow_executor.execute(name=workflow.name, version=workflow.version,
                                             #workflow_input={'name': 'Orkes'})

    #print(f'\nworkflow result: {workflow_run.output["result"]}\n')
    #print(f'see the workflow execution here: {api_config.ui_host}/execution/{workflow_run.workflow_id}\n')
    #task_handler.stop_processes()


if __name__ == '__main__':
    main()
```

Now, you can run the workflow from the UI successfully since we have commented the lines of code to run the workflow and stop the workers.

## Running Workflow in Orkes Conductor

For running the workflow in Orkes Conductor,

- Update the Conductor server URL to your cluster name.

```shell
export CONDUCTOR_SERVER_URL=https://[cluster-name].orkesconductor.io/api
```
(Optionally) If you are using a Conductor server that requires authentication

- [Obtain the key and secret from the Conductor server](https://orkes.io/content/how-to-videos/access-key-and-secret) and replace them with your values.


```shell
export CONDUCTOR_AUTH_KEY=your_key
export CONDUCTOR_AUTH_SECRET=your_key_secret
```

Now, run the application from IDE and view the results from Conductor UI.

> [!NOTE]
> That's it - you just created and executed your first distributed Python app!

## How does the app work?
<img width="1020" alt="Screenshot 2024-03-19 at 14 47 45" src="https://github.com/Srividhya-S-Subramanian/conductor-python-v1/assets/163816773/8cdd4bde-eb39-4dcb-90d0-bc752f374e16">


## Using Conductor in Your Application

There are three main ways you can use Conductor when building durable, resilient, distributed applications.

1. Write service workers that implement business logic to accomplish a specific goal - such as initiating payment transfer, getting user information from the database, etc.
2. Create Conductor workflows that implement application state - A typical workflow implements the saga pattern.
3. Use Conductor SDK and APIs to manage workflows from your application.

### [Create and Run Conductor Workers](workers.md)
### [Create Conductor Workflows](workflows.md)
### [Using Conductor in your Application](conductor_apps.md)
