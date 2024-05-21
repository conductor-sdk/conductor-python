# Conductor OSS Python SDK

Python SDK for working with https://github.com/conductor-oss/conductor.

[Conductor](https://www.conductor-oss.org/) is the leading open-source orchestration platform allowing developers to build highly scalable distributed applications.

Check out the [official documentation for Conductor](https://orkes.io/content).

## ⭐ Conductor OSS

Show support for the Conductor OSS.  Please help spread the awareness by starring Conductor repo.

[![GitHub stars](https://img.shields.io/github/stars/conductor-oss/conductor.svg?style=social&label=Star&maxAge=)](https://GitHub.com/conductor-oss/conductor/)

## Content

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Install Conductor Python SDK](#install-conductor-python-sdk)
  - [Get Conductor Python SDK](#get-conductor-python-sdk)
- [Hello World Application Using Conductor](#hello-world-application-using-conductor)
  - [Step 1: Create Workflow](#step-1-create-workflow)
    - [Creating Workflows by Code](#creating-workflows-by-code)
    - [(Alternatively) Creating Workflows in JSON](#alternatively-creating-workflows-in-json)
  - [Step 2: Write Task Worker](#step-2-write-task-worker)
  - [Step 3: Write _Hello World_ Application](#step-3-write-_hello-world_-application)
- [Running Workflows on Conductor Standalone (Installed Locally)](#running-workflows-on-conductor-standalone-installed-locally)
  - [Setup Environment Variable](#setup-environment-variable)
  - [Start Conductor Server](#start-conductor-server)
  - [Execute Hello World Application](#execute-hello-world-application)
- [Running Workflows on Orkes Conductor](#running-workflows-on-orkes-conductor)
- [Learn More about Conductor Python SDK](#learn-more-about-conductor-python-sdk)
  - [Create and Run Conductor Workers](#create-and-run-conductor-workers)
  - [Create Conductor Workflows](#create-conductor-workflows)
  - [Using Conductor in your Application](#using-conductor-in-your-application)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Install Conductor Python SDK

Before installing Conductor Python SDK, it is a good practice to set up a dedicated virtual environment as follows:

```shell
virtualenv conductor
source conductor/bin/activate
```

### Get Conductor Python SDK

The SDK requires Python 3.9+. To install the SDK, use the following command:

```shell
python3 -m pip install conductor-python
```

## Hello World Application Using Conductor

In this section, we will create a simple "Hello World" application that executes a "greetings" workflow managed by Conductor.

### Step 1: Create Workflow

#### Creating Workflows by Code

Create [greetings_workflow.py](examples/helloworld/greetings_workflow.py) with the following:

```python
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from greetings_worker import greet

def greetings_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    name = 'greetings'
    workflow = ConductorWorkflow(name=name, executor=workflow_executor)
    workflow.version = 1
    workflow >> greet(task_ref_name='greet_ref', name=workflow.input('name'))
    return workflow


```

#### (Alternatively) Creating Workflows in JSON

Create `greetings_workflow.json` with the following:

```json
{
  "name": "greetings",
  "description": "Sample greetings workflow",
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

Workflows must be registered to the Conductor server. Use the API to register the greetings workflow from the JSON file above:
```shell
curl -X POST -H "Content-Type:application/json" \
http://localhost:8080/api/metadata/workflow -d @greetings_workflow.json
```
> [!note]
> To use the Conductor API, the Conductor server must be up and running (see [Running over Conductor standalone (installed locally)](#running-over-conductor-standalone-installed-locally)).

### Step 2: Write Task Worker

Using Python, a worker represents a function with the worker_task decorator. Create [greetings_worker.py](examples/helloworld/greetings_worker.py) file as illustrated below:

> [!note]
> A single workflow can have task workers written in different languages and deployed anywhere, making your workflow polyglot and distributed!

```python
from conductor.client.worker.worker_task import worker_task


@worker_task(task_definition_name='greet')
def greet(name: str) -> str:
    return f'Hello {name}'

```
Now, we are ready to write our main application, which will execute our workflow.

### Step 3: Write _Hello World_ Application

Let's add [helloworld.py](examples/helloworld/helloworld.py) with a `main` method:

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
    # The app is connected to http://localhost:8080/api by default
    api_config = Configuration()

    workflow_executor = WorkflowExecutor(configuration=api_config)

    # Registering the workflow (Required only when the app is executed the first time)
    workflow = register_workflow(workflow_executor)

    # Starting the worker polling mechanism
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
## Running Workflows on Conductor Standalone (Installed Locally)

### Setup Environment Variable

Set the following environment variable to point the SDK to the Conductor Server API endpoint:

```shell
export CONDUCTOR_SERVER_URL=http://localhost:8080/api
```
### Start Conductor Server

To start the Conductor server in a standalone mode from a Docker image, type the command below:

```shell
docker run --init -p 8080:8080 -p 5000:5000 conductoross/conductor-standalone:3.15.0
```
To ensure the server has started successfully, open Conductor UI on http://localhost:5000.

### Execute Hello World Application

To run the application, type the following command:

```
python helloworld.py
```

Now, the workflow is executed, and its execution status can be viewed from Conductor UI (http://localhost:5000).

Navigate to the **Executions** tab to view the workflow execution.

<img width="1434" alt="Screenshot 2024-03-18 at 12 30 07" src="https://github.com/Srividhya-S-Subramanian/conductor-python-v1/assets/163816773/11e829b6-d46a-4b47-b2cf-0bf524a6ebdc">

## Running Workflows on Orkes Conductor

For running the workflow in Orkes Conductor,

- Update the Conductor server URL to your cluster name.

```shell
export CONDUCTOR_SERVER_URL=https://[cluster-name].orkesconductor.io/api
```

- If you want to run the workflow on the Orkes Conductor Playground, set the Conductor Server variable as follows:

```shell
export CONDUCTOR_SERVER_URL=https://play.orkes.io/api
```

- Orkes Conductor requires authentication. [Obtain the key and secret from the Conductor server](https://orkes.io/content/how-to-videos/access-key-and-secret) and set the following environment variables.

```shell
export CONDUCTOR_AUTH_KEY=your_key
export CONDUCTOR_AUTH_SECRET=your_key_secret
```

Run the application and view the execution status from Conductor's UI Console.

> [!NOTE]
> That's it - you just created and executed your first distributed Python app!

## Learn More about Conductor Python SDK

There are three main ways you can use Conductor when building durable, resilient, distributed applications.

1. Write service workers that implement business logic to accomplish a specific goal - such as initiating payment transfer, getting user information from the database, etc.
2. Create Conductor workflows that implement application state - A typical workflow implements the saga pattern.
3. Use Conductor SDK and APIs to manage workflows from your application.

### [Create and Run Conductor Workers](workers.md)
### [Create Conductor Workflows](workflows.md)
### [Using Conductor in your Application](conductor_apps.md)
