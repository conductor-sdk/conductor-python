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
  - [Wait Task](#wait-task)
  - [HTTP Task](#http-task)
  - [Javascript Executor Task](#javascript-executor-task)
  - [JQ Processing](#jq-processing)
- [Executing Workflows](#executing-workflows)
  - [Execute workflow asynchronously](#execute-workflow-asynchronously)
  - [Execute workflow synchronously](#execute-workflow-synchronously)
  - [Execute dynamic workflows using Code](#execute-dynamic-workflows-using-code)
- [Managing Workflow Executions](#managing-workflow-executions)
  - [Get the execution status](#get-the-execution-status)
  - [Update workflow state variables](#update-workflow-state-variables)
  - [Terminate running workflows](#terminate-running-workflows)
  - [Retry failed workflows](#retry-failed-workflows)
  - [Restart workflows](#restart-workflows)
  - [Rerun a workflow from a specific task](#rerun-a-workflow-from-a-specific-task)
  - [Pause a running workflow](#pause-a-running-workflow)
  - [Resume paused workflow](#resume-paused-workflow)
- [Searching for workflows](#searching-for-workflows)
- [Handling Failures, Retries and Rate Limits](#handling-failures-retries-and-rate-limits)
  - [Retries](#retries)
  - [Rate Limits](#rate-limits)
- [Testing your workflows](#testing-your-workflows)
- [Working with Tasks using APIs](#working-with-tasks-using-apis)

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
    set_start_method('fork')
    main()
```

> [!NOTE]
> That's it - you just created your first distributed python app!
> 
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
    return f'order: {order_info.order_id}'

```
## System Tasks
System tasks are the pre-built workers that are available in every Conductor server.

System tasks automates the repeated tasks such as calling an HTTP endpoint, 
executing lightweight ECMA compliant javascript code, publishing to an event broker etc. 

### Wait Task
> [!tip]
> Wait is a powerful way to have your system wait for a certain trigger such as an external event, certain date/time or duration such as 2 hours without having to manage threads, background processes or jobs.

**Using code to create WAIT task**
```python
from conductor.client.workflow.task.wait_task import WaitTask

# waits for 2 seconds before scheduling the next task
wait_for_two_sec = WaitTask(task_ref_name='wait_for_2_sec', wait_for_seconds=2)

# wait until end of jan
wait_till_jan = WaitTask(task_ref_name='wait_till_jsn', wait_until='2024-01-31 00:00 UTC')

# waits until an API call or an event is triggered
wait_for_signal = WaitTask(task_ref_name='wait_till_jan_end')

```
**JSON configuration**
```json
{
  "name": "wait",
  "taskReferenceName": "wait_till_jan_end",
  "type": "WAIT",
  "inputParameters": {
    "until": "2024-01-31 00:00 UTC"
  }
}
```
### HTTP Task
Make a request to an HTTP(S) endpoint. The task allows making GET, PUT, POST, DELETE, HEAD, PATCH requests.

**Using code to create an HTTP task**
```python
from conductor.client.workflow.task.http_task import HttpTask

HttpTask(task_ref_name='call_remote_api', http_input={
        'uri': 'https://orkes-api-tester.orkesconductor.com/api'
    })
```

**JSON configuration**

```json
{
  "name": "http_task",
  "taskReferenceName": "http_task_ref",
  "type" : "HTTP",
  "uri": "https://orkes-api-tester.orkesconductor.com/api",
  "method": "GET"
}
```

### Javascript Executor Task

### JQ Processing

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
> [!note] 
> See [workflow_ops.py](examples/workflow_ops.py) for a fully working application that demonstrates
> working with the workflow executions

Workflows represent te application state.  With Conductor, you can query the workflow execution state anytime during its lifecycle.
You can also send Signals to the workflow that determines the outcome of the workflow state.

[WorkflowClient](src/conductor/client/workflow_client.py) is the client interface used to manage workflow executions.

```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes_clients import OrkesClients

api_config = Configuration()
clients = OrkesClients(configuration=api_config)
workflow_client = clients.get_workflow_client()
```

### Get the execution status
The following method lets you query the status of the workflow execution given the id.
When the `include_tasks` is set the response also includes all the completed and in progress tasks.

`get_workflow(workflow_id: str, include_tasks: Optional[bool] = True) -> Workflow`

### Update workflow state variables
Variables inside a workflow are the equivalent to global variables in a program. 

`update_variables(self, workflow_id: str, variables: dict[str, object] = {})`

### Terminate running workflows
Terminates a running workflow.  Any pending tasks are cancelled and no further work is scheduled for this workflow upon termination.
A failure workflow will be triggered, but can be avoided if `trigger_failure_workflow` is set to False.

`terminate_workflow(self, workflow_id: str, reason: Optional[str] = None, trigger_failure_workflow: bool = False)`

### Retry failed workflows
If the workflow has failed due to one of the task failure after exhausting the retries for the task, the workflow can 
still be resumed by calling the retry.

`retry_workflow(self, workflow_id: str, resume_subworkflow_tasks: Optional[bool] = False)`

When a sub-workflow inside a workflow has failed, there are two options:
1. re-trigger the sub-workflow from the start (Default behavior)
2. resume the sub-workflow from the failed task (set `resume_subworkflow_tasks` to `True`)

``
### Restart workflows
A workflow in the terminal state (COMPLETED, TERMINATED, FAILED) can be restarted from the beginning. 
Useful when retrying from the last failed task is not enough and the whole workflow needs to be started again.

`restart_workflow(self, workflow_id: str, use_latest_def: Optional[bool] = False)`

### Rerun a workflow from a specific task
In the cases where a worflow needs to be restarted from a specific task rather than from the beginning, `re-run` provides that option.
When issuing the re-run command to the workflow, you have the ability to specify the id of the task from where the workflow 
should be restarted (as opposed to from the beginning) and optionally, the input of the workflow can also be changed:

`rerun_workflow(self, workflow_id: str, rerun_workflow_request: RerunWorkflowRequest)`

> [!tip]
> re-run is one of the most powerful feature Conductor has, givingin you unparalleled control over the workflow restart
> 

### Pause a running workflow
A running workflow can be put to a PAUSED status.  A paused workflow lets the currently running tasks complete, 
but does not schedule any new tasks until resumed.

`pause_workflow(self, workflow_id: str)`

### Resume paused workflow
Resume operation resumes the currently paused workflow, immediately evaluating its state and scheduling the next set of
tasks.

`resume_workflow(self, workflow_id: str)`

## Searching for workflows
Workflow executions are retained until removed from Conductor.  This gives complete visibility into all the executions an 
application has - regardless of the number of executions.  Conductor has a poewrful search API that allows you to search 
for workflow executions. 

`search(self, start, size, free_text: str = '*', query: str = None) -> ScrollableSearchResultWorkflowSummary`

* **free_text**: Free text search to look for specific words in the workflow and task input/output
* **query** SQL like query to search against specific fields in the workflow. 

Supported fields for **query**

| field       | description     |
|-------------|-----------------|
| status      |workflow status  |
| correlationId |correlation Id   |
| workflowType |name of the workflow |
 | version     |workflow version |
|startTime|start time of the workflow in unix millis|


## Handling Failures, Retries and Rate Limits
Conductor lets you embrace failures rather than worry about failures and complexities that are introduced in the system
to handle failures.

All the aspect of handling failures, retries, rate limits etc. are driven by the configuration that can be updated in 
real-time without having to re-deploy your application.

### Retries
Each task in Conductor workflow can be configured to handle failures with retries, 
along with the retry policy (linear, fixed, exponential backoff) and max. number of retry attempts allowed.

See [Error Handling](https://orkes.io/content/error-handling) for more details.

### Rate Limits
What happens when a task is operating on a critical resource that can only handle so many requests at a time?
Tasks can be configured to have a fixed concurrency (X request at a time) or a rate (Y tasks / time window).

**Task Registration**
```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import TaskDef
from conductor.client.orkes_clients import OrkesClients


def main():
    api_config = Configuration()
    clients = OrkesClients(configuration=api_config)
    metadata_client = clients.get_metadata_client()

    task_def = TaskDef()
    task_def.name = 'task_with_retries'
    task_def.retry_count = 3
    task_def.retry_logic = 'LINEAR_BACKOFF'
    task_def.retry_delay_seconds = 1

    # only allow 3 tasks at a time to be in the IN_PROGRESS status
    task_def.concurrent_exec_limit = 3

    # timeout the task if not polled within 60 seconds of scheduling
    task_def.poll_timeout_seconds = 60

    # timeout the task if the task does not COMPLETE in 2 minutes
    task_def.timeout_seconds = 120

    # for the long running tasks, timeout if the task does not get updated in COMPLETED or IN_PROGRESS status in
    # 60 seconds after the last update
    task_def.response_timeout_seconds = 60

    # only allow 100 executions in a 10-second window! -- Note, this is complementary to concurrent_exec_limit
    task_def.rate_limit_per_frequency = 100
    task_def.rate_limit_frequency_in_seconds = 10

    metadata_client.register_task_def(task_def=task_def)
```


```json
{
  "name": "task_with_retries",
  
  "retryCount": 3,
  "retryLogic": "LINEAR_BACKOFF",
  "retryDelaySeconds": 1,
  "backoffScaleFactor": 1,
  
  "timeoutSeconds": 120,
  "responseTimeoutSeconds": 60,
  "pollTimeoutSeconds": 60,
  "timeoutPolicy": "TIME_OUT_WF",
  
  "concurrentExecLimit": 3,
  
  "rateLimitPerFrequency": 0,
  "rateLimitFrequencyInSeconds": 1
}
```
Update the task definition:
```shell
POST /api/metadata/taskdef -d @task_def.json
```

See [task_configure.py](examples/task_configure.py) for a detailed working app.

## Testing your workflows

## Working with Tasks using APIs





