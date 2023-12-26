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
- [Start Conductor Server](#start-conductor-server)
- [Build a conductor workflow based application](#build-a-conductor-workflow-based-application)
  - [Step 1: Create a Workflow](#step-1-create-a-workflow)
  - [Step 2: Write Worker](#step-2-write-worker)
  - [Step 3: Write _your_ application](#step-3-write-_your_-application)
- [Implementing Workers](#implementing-workers)
- [System Tasks](#system-tasks)
  - [HTTP Task](#http-task)
  - [Wait Task](#wait-task)
  - [JQ Processing](#jq-processing)
  - [Javascript Executor Task](#javascript-executor-task)
- [Executing Workflows](#executing-workflows)
  - [Execute workflow asynchronously](#execute-workflow-asynchronously)
  - [Execute workflow synchronously](#execute-workflow-synchronously)
  - [Execute dynamic workflows using Code](#execute-dynamic-workflows-using-code)
- [Managing Workflow Executions](#managing-workflow-executions)
  - [Get the execution status](#get-the-execution-status)
  - [Update a task in the workflow](#update-a-task-in-the-workflow)
  - [Update workflow state variables](#update-workflow-state-variables)
  - [Terminate running workflows](#terminate-running-workflows)
  - [Retry failed workflows](#retry-failed-workflows)
  - [Restart workflows](#restart-workflows)
  - [Rerun a workflow from a specific task](#rerun-a-workflow-from-a-specific-task)
  - [Pause a running workflow](#pause-a-running-workflow)
  - [Resume paused workflow](#resume-paused-workflow)
- [Searching for workflows](#searching-for-workflows)
- [Testing your workflows](#testing-your-workflows)
- [Eventing Support with Kafka, AMQP, NATS, SQS](#eventing-support-with-kafka-amqp-nats-sqs)
- [](#)

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
curl -X POST -H "Content-Type:application/json" \
http://localhost:8080/api/metadata/workflow -d @workflow.json
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
## System Tasks
System tasks are the pre-built workers that are available in every Conductor server.  
These are commonly used task workers which are generic in nature and battle tested by Conductor community over the years.

### HTTP Task

### Wait Task
### JQ Processing
### Javascript Executor Task


## Executing Workflows
[WorkflowClient](src/conductor/client/workflow_client.py) interface provides all the APIs required to work with workflow executions.
```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes_clients import OrkesClients

api_config = Configuration()
clients = OrkesClients(configuration=api_config)
workflow_client = clients.get_workflow_client() 
```
### Execute workflow asynchronously
Useful when workflows are long-running  
```python
from conductor.client.http.models import StartWorkflowRequest

request = StartWorkflowRequest()
request.name = 'hello'
request.version = 1
request.input = {'name': 'Orkes'}
# workflow id is the unique execution id associated with this execution
workflow_id = workflow_client.start_workflow(request)
```
### Execute workflow synchronously
Useful when workflows complete very quickly - usually under 20-30 second
```python
from conductor.client.http.models import StartWorkflowRequest

request = StartWorkflowRequest()
request.name = 'hello'
request.version = 1
request.input = {'name': 'Orkes'}

workflow_run = workflow_client.execute_workflow(
        start_workflow_request=request, 
        wait_for_seconds=12)
```
### Execute dynamic workflows using Code
For cases, where the workflows cannot be created statically ahead of the time, 
Conductor is a powerful dynamic workflow execution platform that lets you create
very complex workflows in code and execute them.  Useful when the workflow is unique for each execution.

```python
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes_clients import OrkesClients
from conductor.client.worker.worker_task import worker_task
from conductor.client.workflow.conductor_workflow import ConductorWorkflow


workflow = ConductorWorkflow(name='dynamic_workflow', version=1, executor=workflow_executor)
get_email = get_user_email(task_ref_name='get_user_email_ref', userid=workflow.input('userid'))
sendmail = send_email(task_ref_name='send_email_ref', email=get_email.output('result'), subject='Hello from Orkes',
                      body='Test Email')
workflow >> get_email >> sendmail

# Execute the workflow and get the workflow run result
result = workflow.execute(workflow_input={'userid': 'usera'})

# Print the workflow status
print(f'workflow completed with status {result.status}')

```
see [dynamic_workflow.py](examples/dynamic_workflow.py) for a fully functional example.

**For more complex workflow example with all the supported features, see [kitchensink.py](examples/kitchensink.py)**

## Managing Workflow Executions

### Get the execution status
### Update a task in the workflow
### Update workflow state variables
### Terminate running workflows
### Retry failed workflows
### Restart workflows
### Rerun a workflow from a specific task
### Pause a running workflow
### Resume paused workflow

## Searching for workflows

## Testing your workflows
## Eventing Support with Kafka, AMQP, NATS, SQS
## 



