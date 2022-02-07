# Conductor Python

Software Development Kit for Netflix Conductor, written on Python.

## Set up Conductor

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

## Install Python SDK package

// TODO

## Run

### Create new task

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

### Create new workflow

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
    ```bash
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

### Start new workflow

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

### See workflow execution

Now you must be able to see its execution through the UI.
* URL: 
  * prefix: `http://localhost:5001/execution`
  * suffix: `${workflow_id}`
* Example: `http://localhost:5001/execution/8ff0bc06-4413-4c94-b27a-b3210412a914`
