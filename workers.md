# Writing Workers

A Workflow task represents a unit of business logic that achieves a specific goal such as check inventory, initiate payment transfer etc.
Worker implements a task in the workflow.  (note: _often times worker and task are used interchangeably in various blogs, docs etc._)

## Content

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Implementing Workers](#implementing-workers)
  - [Managing workers in _your_ application](#managing-workers-in-_your_-application)
- [Design Principles for Workers](#design-principles-for-workers)
- [System Task Workers](#system-task-workers)
  - [Wait Task](#wait-task)
  - [HTTP Task](#http-task)
  - [Javascript Executor Task](#javascript-executor-task)
  - [Json Processing using JQ](#json-processing-using-jq)
- [Worker vs Microservice / HTTP endpoints](#worker-vs-microservice--http-endpoints)
- [Deploying Workers in production](#deploying-workers-in-production)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 

## Implementing Workers
The workers can be implemented by writing a simple python function and annotating the function with the `@worker_task`
Conductor workers are services (similar to microservices) that follow [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single_responsibility_principle)

Workers can be hosted along with the workflow or running a distributed environment where a single workflow uses workers 
that are deployed and running in different machines/vms/containers.  Whether to keep all the workers in the same application or 
run them as distributed application is a design and architectural choice.  Conductor is well suited for both kind of scenarios.

You create or convert any existing python function to a distributed worker by adding `@worker_task` annotation to it.
Here is a simple worker that takes `name` as input and returns greetings:

```python
from conductor.client.worker.worker_task import worker_task

@worker_task(task_definition_name='greetings')
def greetings(name: str) -> str:
    return f'Hello, {name}'
```

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

### Managing workers in _your_ application
Workers use a polling mechanism (with long-poll) to check for any available tasks periodically from server.
The startup and shutdown of workers is handled by `conductor.client.automator.task_handler.TaskHandler` class.

```python
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration

def main():
    # points to http://localhost:8080/api by default
    api_config = Configuration()

    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
        import_modules=['greetings']  # import workers from this module - leave empty if all the workers are in the same module
    )
    
    # start worker polling
    task_handler.start_processes()

    # Call to stop the workers when the application is ready to shutdown
    task_handler.stop_processes()


if __name__ == '__main__':
    main()

```

## Design Principles for Workers
Each worker embodies design pattern and follows certain basic principles:

1. Workers are stateless and do not implement a workflow specific logic.
2. Each worker executes a very specific task and produces well-defined output given specific inputs.
3. Workers are meant to be idempotent (or should handle cases where the task that partially executed gets rescheduled due to timeouts etc.)
4. Workers do not implement the logic to handle retries etc., that is taken care by the Conductor server.

## System Task Workers
A system task worker is a pre-built, general purpose worker that is part of your Conductor server distribution.

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
Execute ECMA compliant Javascript code.  Useful when you need to write a script to do data mapping, calculations etc.


```python
from conductor.client.workflow.task.javascript_task import JavascriptTask

say_hello_js = """
function greetings() {
    return {
        "text": "hello " + $.name
    }
}
greetings();
"""

js = JavascriptTask(task_ref_name='hello_script', script=say_hello_js, bindings={'name': '${workflow.input.name}'})
```

```json
{
  "name": "inline_task",
  "taskReferenceName": "inline_task_ref",
  "type": "INLINE",
  "inputParameters": {
    "expression": " function greetings() {\n  return {\n            \"text\": \"hello \" + $.name\n        }\n    }\n    greetings();",
    "evaluatorType": "graaljs",
    "name": "${workflow.input.name}"
  }
}
```

### Json Processing using JQ
[jq](https://jqlang.github.io/jq/) is like sed for JSON data - you can use it to slice and filter and map and transform 
structured data with the same ease that sed, awk, grep and friends let you play with text.

```python
from conductor.client.workflow.task.json_jq_task import JsonJQTask

jq_script = """
{ key3: (.key1.value1 + .key2.value2) }
"""

jq = JsonJQTask(task_ref_name='jq_process', script=jq_script)
```

```json
{
  "name": "json_transform_task",
  "taskReferenceName": "json_transform_task_ref",
  "type": "JSON_JQ_TRANSFORM",
  "inputParameters": {
    "key1": "k1",        
    "key2": "k2",
    "queryExpression": "{ key3: (.key1.value1 + .key2.value2) }",
  }
}
```

## Worker vs Microservice / HTTP endpoints

> [!tip] 
> Workers are a lightweight alternative to exposing an HTTP endpoint and orchestrating using `HTTP` task. 
>  Using workers is a recommended approach if you do not need to expose the service over HTTP or gRPC endpoints.

There are several advantages to this approach:
1. **No need for an API management layer** : Given there are no exposed endpoints and workers are self load-balancing.
2. **Reduced infrastructure footprint** :  No need for an API gateway/load balancer.
3. All the communication is initiated from worker using polling - avoiding need to open up any incoming TCP ports.
4. Workers **self-regulate** when busy, they only poll as much as they can handle.  Backpressure handling is done out of the box.
5. Workers can be scale up / down easily based on the demand by increasing the no. of processes.

## Deploying Workers in production
Conductor workers can run in cloud-native environment or on-prem and can easily be deployed like any other python application.
Workers can run a containerized environment, VMs or on bare-metal just like you would deploy your other python applications.



