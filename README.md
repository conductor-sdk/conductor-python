# Conductor Python

Software Development Kit for Netflix Conductor, written on and providing support for Python.

## Quick Guide

In case you have already set up Conductor and got it running, you can quickly onboard to it with these steps:
1. Install Conductor Python SDK from pypi:
    ```shell
    $ python3 -m pip install conductor-python
    ```
2. Run Conductor Python SDK:
    ```shell
    $ python3 -m conductor.client
    ```

### Custom worker

In order to create a custom python worker, it should inherit from `WorkerInterface` and instantiate a `TaskHandler` object.

Here is an example:

* Worker:
  * Details:
    ```python
    from conductor.client.worker.worker_interface import WorkerInterface
    import multiprocessing
    import socket


    class SimplePythonWorker(WorkerInterface):
        def get_task_definition_name(self):
            return 'simple_python_worker'

        def execute(self, task_result):
            task_result.add_output_data('hostname', socket.gethostname())
            task_result.add_output_data('cpu_cores', multiprocessing.cpu_count())
            return task_result

        def get_polling_interval(self):
            return 3
    ```
    * Name: `simple_python_worker`
    * Input: `None`
    * Output: [`hostname`, `cpu_cores`]
    * Polling Interval: `3s`
* Main:
    ```python
    from conductor.client.automator.task_handler import TaskHandler
    from conductor.client.worker.simple_python_worker import SimplePythonWorker


    def main():
        workers = [SimplePythonWorker()] * 1
        with TaskHandler(workers) as parallel_task_handler:
            parallel_task_handler.start()


    if __name__ == '__main__':
        main()
    ```
    * Single worker within TaskHandler

## Full installation guide

### Set up Conductor

1. Clone Netflix Conductor repository: https://github.com/Netflix/conductor
    ```shell
    $ git clone https://github.com/Netflix/conductor.git
    ```
2. Start Conductor server by running this command at the repo root folder (`/conductor`):
    ```shell
    $ ./gradlew bootRun
    ```
3. Start Conductor UI by running this command at the UI folder (`/conductor/ui`):
    ```shell
    $ yarn install
    $ yarn run start
    ```

You should be able to access:
* Conductor API:
  * http://localhost:8080/swagger-ui/index.html
* Conductor UI:
  * http://localhost:5000

### Run

#### Create new task

You need to define a *Task* within *Conductor* that your `Python Worker` is capable of running.

Make a POST request to `/metadata/taskdefs` endpoint at your conductor server.
* URL example: `http://localhost:8080/api/metadata/taskdefs`
* Task Definition example:
    ```json
    [
      {
        "name": "simple_python_worker",
        "description": "Simple Python Worker",
        "retryCount": 3,
        "retryLogic": "FIXED",
        "retryDelaySeconds": 10,
        "timeoutSeconds": 300,
        "timeoutPolicy": "TIME_OUT_WF",
        "responseTimeoutSeconds": 180,
        "ownerEmail": "example@example.com"
      }
    ]
    ```
* Command example:
    ```shell
    $ curl -X 'POST' \
        'http://localhost:8080/api/metadata/taskdefs' \
        -H 'accept: */*' \
        -H 'Content-Type: application/json' \
        -d '[
        {
          "name": "simple_python_worker",
          "description": "Simple Python Worker",
          "retryCount": 3,
          "retryLogic": "FIXED",
          "retryDelaySeconds": 10,
          "timeoutSeconds": 300,
          "timeoutPolicy": "TIME_OUT_WF",
          "responseTimeoutSeconds": 180,
          "ownerEmail": "example@example.com"
        }
      ]'
    ```

#### Create new workflow

You need to define a *Workflow* within *Conductor* that contains the *Task* you had just defined.

Make a POST request to `/metadata/workflow` endpoint at your conductor server.
* URL example: `http://localhost:8080/api/metadata/workflow`
* Workflow Definition example:
    ```json
    {
      "createTime": 1634021619147,
      "updateTime": 1630694890267,
      "name": "simple_workflow_with_python_worker",
      "description": "Simple Workflow with Python Worker",
      "version": 1,
      "tasks": [
        {
          "name": "simple_python_worker",
          "taskReferenceName": "simple_python_worker_ref_1",
          "inputParameters": {},
          "type": "SIMPLE"
        }
      ],
      "inputParameters": [],
      "outputParameters": {
        "workerOutput": "${simple_python_worker_ref_1.output}"
      },
      "schemaVersion": 2,
      "restartable": true,
      "ownerEmail": "example@example.com",
      "timeoutPolicy": "ALERT_ONLY",
      "timeoutSeconds": 0
    }
    ```
* Command example:
    ```shell
    $ curl -X 'POST' \
        'http://localhost:8080/api/metadata/workflow' \
        -H 'accept: */*' \
        -H 'Content-Type: application/json' \
        -d '{
        "createTime": 1634021619147,
        "updateTime": 1630694890267,
        "name": "simple_workflow_with_python_worker",
        "description": "Simple Workflow with Python Worker",
        "version": 1,
        "tasks": [
          {
            "name": "simple_python_worker",
            "taskReferenceName": "simple_python_worker_ref_1",
            "inputParameters": {},
            "type": "SIMPLE"
          }
        ],
        "inputParameters": [],
        "outputParameters": {
          "workerOutput": "${simple_python_worker_ref_1.output}"
        },
        "schemaVersion": 2,
        "restartable": true,
        "ownerEmail": "example@example.com",
        "timeoutPolicy": "ALERT_ONLY",
        "timeoutSeconds": 0
      }'
    ```

#### Start new workflow

Now that you have defined a *Task* and a *Workflow* within *Conductor*, you should be able to run it.

Make a POST request to `/workflow/{name}` endpoint at your conductor server.
* URL example: `http://localhost:8080/api/workflow/simple_workflow_with_python_worker`
  * Priority should be empty
  * Request body should be empty, like: `{}`
* Command example:
    ```shell
    $ curl -X 'POST' \
        'http://localhost:8080/api/workflow/simple_workflow_with_python_worker' \
        -H 'accept: text/plain' \
        -H 'Content-Type: application/json' \
        -d '{}'
    ```
* Create a bunch of workflows:
    ```shell
    $ export CREATE_WORKFLOW_SHORTCUT="curl -X 'POST' \
        'http://localhost:8080/api/workflow/simple_workflow_with_python_worker' \
        -H 'accept: text/plain' \
        -H 'Content-Type: application/json' \
        -d '{}' \
        -s"
    
    $ for idx in {1..100}; do \
        echo "Creating workflow ${idx}"; \
        workflow_id=$(eval "${CREATE_WORKFLOW_SHORTCUT}"); \
        echo "workflow_id=${workflow_id}"; \
      done
    ```
    * Expected output example:
        ```shell
        Creating workflow 1
        workflow_id=6dd2c86b-5ce6-487a-9a65-632139da1345
        Creating workflow 2
        workflow_id=b0ddfdcf-0c4a-4fd3-892c-97fc38c46d63
        ...
        ```

You should receive a *Workflow ID* at the *Response body*
* *Workflow ID* example: `8ff0bc06-4413-4c94-b27a-b3210412a914`

#### See workflow execution

Now you must be able to see its execution through the UI.
* URL: 
  * prefix: `http://localhost:5001/execution`
  * suffix: `${workflow_id}`
* Example: `http://localhost:5001/execution/8ff0bc06-4413-4c94-b27a-b3210412a914`
