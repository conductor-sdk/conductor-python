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
- [Simple Hello World Application using Conductor](#simple-hello-world-application-using-conductor)
  - [Step 1: Create a Workflow](#step-1-create-a-workflow)
  - [Step 2: Write Worker](#step-2-write-worker)
  - [Step 3: Write _your_ application](#step-3-write-_your_-application)
- [Using Conductor in your application](#using-conductor-in-your-application)
  - [Create and Run Conductor Workers](#create-and-run-conductor-workers)
  - [Create Conductor Workflows](#create-conductor-workflows)
  - [Using Conductor in your Application](#using-conductor-in-your-application)
- [Running your distributed workflow](#running-your-distributed-workflow)
  - [Setup SDK](#setup-sdk)
  - [Start Conductor Server](#start-conductor-server)
- [Run the workflow on Orkes](#run-the-workflow-on-Orkes)
  
  

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
## Simple Hello World Application using Conductor
In this section, we will create a simple "Hello World" application that uses Conductor. 

### Step 1: Create a [Workflow](workflows.md)

**Use Code to create workflows**

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

### Step 2: Write [Worker](workers.md)

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
## Running your distributed workflow

### Setup SDK

Point the SDK to the Conductor Server API endpoint. Now, let's test the app locally.
```shell
export CONDUCTOR_SERVER_URL=http://localhost:8080/api
```
### Start Conductor Server
```shell
docker run --init -p 8080:8080 -p 5000:5000 conductoross/conductor-standalone:3.15.0
```
After starting the server navigate to http://localhost:5000 to ensure the server has started successfully. Go ahead and run your code.
```
python greetings_workflow.py
```
Now, the workflow gets executed and the result can be observed by opening http:localhost:5000/ in your Web Browser as shown below. 'hello' workflow has been created. Open the executions tab and notice that hello workflow has been executed. 
<img width="1434" alt="Screenshot 2024-03-18 at 12 30 07" src="https://github.com/Srividhya-S-Subramanian/conductor-python-v1/assets/163816773/11e829b6-d46a-4b47-b2cf-0bf524a6ebdc">

Open the Workbench tab and try running the 'hello' workflow. You will notice that the workflow execution fails. This is because task_handler.stop_processes() [greetings_main.py], stops all the workers. So, workers are not available to execute the tasks.

Now, let's update greetings_main.py

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
Now, you can run the workflow from the UI successfully, since we have commented the lines of code used to run the workflow and stop the workers.

## Run the workflow on Orkes
Update the Conductor Server URL. 
```shell
export CONDUCTOR_SERVER_URL=https://[cluster-name].orkesconductor.io/api
```
(Optionally) If you are using a Conductor server that requires authentication

[How to obtain the key and secret from the conductor server
](https://orkes.io/content/docs/getting-started/concepts/access-control)


```shell
export CONDUCTOR_AUTH_KEY=your_key
export CONDUCTOR_AUTH_SECRET=your_key_secret
```
> [!NOTE]
> That's it - you just created and executed your first distributed workflow!

## How does the app work?
<img width="1020" alt="Screenshot 2024-03-19 at 14 47 45" src="https://github.com/Srividhya-S-Subramanian/conductor-python-v1/assets/163816773/8cdd4bde-eb39-4dcb-90d0-bc752f374e16">


## Using Conductor in your application
There are three main ways you will use Conductor when building durable, resilient, distributed applications.
1. Write service workers that implements business logic to accomplish a specific goal - such as initiate payment transfer, get user information from database etc. 
2. Create Conductor workflows that implements application state - A typical workflow implements SAGA pattern
3. Use Conductor SDK and APIs to manage workflows from your application.

In this guide, we will dive deeper into each of these topic.

### [Create and Run Conductor Workers](workers.md)
### [Create Conductor Workflows](workflows.md)
### [Using Conductor in your Application](conductor_apps.md)









