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

In order to:
* Create a custom python worker, it should inherit from `WorkerInterface` and implement the execution method. Example:
  ```python
  from conductor.client.http.models.task_result import TaskResult
  from conductor.client.worker.worker_interface import WorkerInterface


  class SimplePythonWorker(WorkerInterface):
      def __init__(self):
          super().__init__('simple_python_worker')

      def execute(self, task):
          task_result = TaskResult(
              task_id=task.task_id,
              workflow_instance_id=task.workflow_instance_id,
              worker_id=self.get_task_definition_name()
          )
          self.__execute(task_result)
          task_result.status = 'COMPLETED'
          return task_result

      def __execute(self, task_result):
          task_result.add_output_data('key', 'value')
  ```
* Run, you should create a main method to instantiate a `TaskHandler` object with your implemented workers. Example:
    ```python
    from conductor.client.automator.task_handler import TaskHandler
    from conductor.client.configuration.configuration import Configuration
    from conductor.client.worker.sample.simple_python_worker import SimplePythonWorker
    import logging

    logger = logging.getLogger(
        Configuration.get_logging_formatted_name(
            __name__
        )
    )


    def main():
        configuration = Configuration(
            debug=True
        )
        configuration.apply_logging_config()
        workers = [SimplePythonWorker()] * 3
        logger.debug(f'Created workers: {workers}')
        with TaskHandler(configuration, workers) as task_handler:
            logger.debug(f'Created task_handler: {task_handler}')
            task_handler.start()


    if __name__ == '__main__':
        main()
    ```

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

### Test

#### Unit Testing

In order to run unit testing, go to `src` folder from repository root folder and run:

```shell
$ python3 -m unittest -v
test_execute_task (tst.automator.test_task_runner.TestTaskRunner) ... ok
test_execute_task_with_faulty_execution_worker (tst.automator.test_task_runner.TestTaskRunner) ... ok
test_execute_task_with_invalid_task (tst.automator.test_task_runner.TestTaskRunner) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```