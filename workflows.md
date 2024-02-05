# Conductor Workflows
Workflow can be defined as the collection of tasks and operators that specifies the order and execution of the defined tasks. 
This orchestration occurs in a hybrid ecosystem that encircles serverless functions, microservices, and monolithic applications. 

In this section, we will dive deeper into creating and executing Conductor workflows using Python SDK.

[![GitHub stars](https://img.shields.io/github/stars/conductor-oss/conductor.svg?style=social&label=Star&maxAge=)](https://GitHub.com/conductor-oss/conductor/)

## Content

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Creating Workflows](#creating-workflows)
  - [Execute dynamic workflows using Code](#execute-dynamic-workflows-using-code)
  - [Kitchensink Workflow](#kitchensink-workflow)
- [Executing Workflows](#executing-workflows)
  - [Execute workflow asynchronously](#execute-workflow-asynchronously)
  - [Execute workflow synchronously](#execute-workflow-synchronously)
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

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Creating Workflows
Conductor lets you create the workflows either using Python or JSON as the configuration.  
Using Python as code to define and execute workflows let you build extremely powerful, dynamic workflows and run them on Conductor.

When the workflows are fairly static, they can be designed using the Orkes UI (available when using orkes.io) and using APIs or SDKs to register and run the workflows.

Both the code and configuration approaches are equally powerful and similar in nature to how you treat Infrastructure as Code.

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


@worker_task(task_definition_name='get_user_email')
def get_user_email(userid: str) -> str:
    return f'{userid}@example.com'


@worker_task(task_definition_name='send_email')
def send_email(email: str, subject: str, body: str):
    print(f'sending email to {email} with subject {subject} and body {body}')


def main():

    # defaults to reading the configuration using following env variables
    # CONDUCTOR_SERVER_URL : conductor server e.g. https://play.orkes.io/api
    # CONDUCTOR_AUTH_KEY : API Authentication Key
    # CONDUCTOR_AUTH_SECRET: API Auth Secret
    api_config = Configuration()

    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()

    clients = OrkesClients(configuration=api_config)
    workflow_executor = clients.get_workflow_executor()
    workflow = ConductorWorkflow(name='dynamic_workflow', version=1, executor=workflow_executor)
    get_email = get_user_email(task_ref_name='get_user_email_ref', userid=workflow.input('userid'))
    sendmail = send_email(task_ref_name='send_email_ref', email=get_email.output('result'), subject='Hello from Orkes',
                          body='Test Email')
    workflow >> get_email >> sendmail

    # Configure the output of the workflow
    workflow.output_parameters(output_parameters={
        'email': get_email.output('result')
    })

    result = workflow.execute(workflow_input={'userid': 'user_a'})
    print(f'\nworkflow output:  {result.output}\n')
    task_handler.stop_processes()


if __name__ == '__main__':
    main()

```

```shell
>> python3 dynamic_workflow.py 

2024-02-03 19:54:35,700 [32853] conductor.client.automator.task_handler INFO     created worker with name=get_user_email and domain=None
2024-02-03 19:54:35,781 [32853] conductor.client.automator.task_handler INFO     created worker with name=send_email and domain=None
2024-02-03 19:54:35,859 [32853] conductor.client.automator.task_handler INFO     TaskHandler initialized
2024-02-03 19:54:35,859 [32853] conductor.client.automator.task_handler INFO     Starting worker processes...
2024-02-03 19:54:35,861 [32853] conductor.client.automator.task_runner INFO     Polling task get_user_email with domain None with polling interval 0.1
2024-02-03 19:54:35,861 [32853] conductor.client.automator.task_handler INFO     Started 2 TaskRunner process
2024-02-03 19:54:35,862 [32853] conductor.client.automator.task_handler INFO     Started all processes
2024-02-03 19:54:35,862 [32853] conductor.client.automator.task_runner INFO     Polling task send_email with domain None with polling interval 0.1
sending email to user_a@example.com with subject Hello from Orkes and body Test Email

workflow output:  {'email': 'user_a@example.com'}

2024-02-03 19:54:36,309 [32853] conductor.client.automator.task_handler INFO     Stopped worker processes...
```
see [dynamic_workflow.py](examples/dynamic_workflow.py) for a fully functional example.

see [kitchensink.py](examples/kitchensink.py) for a more complex example. 

### Kitchensink Workflow 
For more complex workflow example with all the supported features, see [kitchensink.py](examples/kitchensink.py)

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
Useful when workflows are long-running.
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
Useful when workflows complete very quickly - usually under 20-30 second.
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


## Managing Workflow Executions
> [!note] 
> See [workflow_ops.py](examples/workflow_ops.py) for a fully working application that demonstrates
> working with the workflow executions and sending signals to the workflow to manage its state.

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
In the cases where a workflow needs to be restarted from a specific task rather than from the beginning, `re-run` provides that option.
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






