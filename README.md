# Conductor Python

Software Development Kit for Netflix Conductor, written on and providing support for Python.

## Quick Guide

1. Create a virtual environment
    ```shell
    $ virtualenv conductor
    $ source conductor/bin/activate
    $ python3 -m pip list
    Package    Version
    ---------- -------
    pip        22.0.3
    setuptools 60.6.0
    wheel      0.37.1
    ```
1. Install latest version of `conductor-python` from pypi
    ```shell
    $ python3 -m pip install conductor-python
    Collecting conductor-python
    Collecting certifi>=14.05.14
    Collecting urllib3>=1.15.1
    Requirement already satisfied: setuptools>=21.0.0 in ./conductor/lib/python3.8/site-packages (from conductor-python) (60.6.0)
    Collecting six>=1.10
    Installing collected packages: certifi, urllib3, six, conductor-python
    Successfully installed certifi-2021.10.8 conductor-python-1.0.7 six-1.16.0 urllib3-1.26.8
    ```
2. Create a worker capable of executing a `Task`. Example:
    ```python
    from conductor.client.http.models.task import Task
    from conductor.client.http.models.task_result import TaskResult
    from conductor.client.http.models.task_result_status import TaskResultStatus
    from conductor.client.worker.worker_interface import WorkerInterface


    class SimplePythonWorker(WorkerInterface):
        def execute(self, task: Task) -> TaskResult:
            task_result = self.get_task_result_from_task(task)
            task_result.add_output_data('key', 'value')
            task_result.status = TaskResultStatus.COMPLETED
            return task_result
    ```
    * The `add_output_data` is the most relevant part, since you can store information in a dictionary, which will be sent within `TaskResult` as your execution response to Conductor
3. Create a main method to start polling tasks to execute with your worker. Example:
    ```python
    from conductor.client.automator.task_handler import TaskHandler
    from conductor.client.example.worker.cpp.simple_cpp_worker import SimpleCppWorker
    from conductor.client.example.worker.python.simple_python_worker import SimplePythonWorker


    def main():
        workers = [
            SimpleCppWorker('cpp_task_example'),
            SimplePythonWorker('python_task_example')
        ]
        with TaskHandler(workers) as task_handler:
            task_handler.start_processes()
            task_handler.join_processes()


    if __name__ == '__main__':
        main()
    ```
    * This example contains two workers, each with a different execution method, capable of running the same `task_definition_name`
    * You can pass a `Configuration` object to `TaskHandler`, where you can set:
      * `base_url`: like `localhost:8000/api`
      * `debug`: true/false
      * `AuthenticationSettings`:
        ```
        authentication_settings=AuthenticationSettings(
            key_id='id',
            key_secret='secret'
        )
        ```
    * You can pass a `MetricsSettings` object to `TaskHandler`, where you can set:
        ```
        metrics_settings=MetricsSettings(
            directory='.',
            file_name='metrics.log', 
            update_interval=0.1
        )
        ```
4. Now that you have implemented the example, you can start the Conductor server locally:
      1. Clone [Netflix Conductor repository](https://github.com/Netflix/conductor):
          ```shell
          $ git clone https://github.com/Netflix/conductor.git
          $ cd conductor/
          ```
      2. Start the Conductor server:
          ```shell
          /conductor$ ./gradlew bootRun
          ```
      3. Start Conductor UI:
          ```shell
          /conductor$ cd ui/
          /conductor/ui$ yarn install
          /conductor/ui$ yarn run start
          ```
      You should be able to access:
      * Conductor API:
        * http://localhost:8080/swagger-ui/index.html
      * Conductor UI:
        * http://localhost:5000
5. Create a `Task` within `Conductor`:
    ```json
    {
        "name": "python_task_example",
        "description": "Python task example",
        "retryCount": 3,
        "retryLogic": "FIXED",
        "retryDelaySeconds": 10,
        "timeoutSeconds": 300,
        "timeoutPolicy": "TIME_OUT_WF",
        "responseTimeoutSeconds": 180,
        "ownerEmail": "example@example.com"
    }
    ```
6. Create a `Workflow` within `Conductor`:
    ```json
    {
        "name": "workflow_with_python_task_example",
        "description": "Workflow with Python Task example",
        "version": 1,
        "tasks": [
          {
            "name": "python_task_example",
            "taskReferenceName": "python_task_example_ref_1",
            "inputParameters": {},
            "type": "SIMPLE"
          }
        ],
        "inputParameters": [],
        "outputParameters": {
          "workerOutput": "${python_task_example_ref_1.output}"
        },
        "schemaVersion": 2,
        "restartable": true,
        "ownerEmail": "example@example.com",
        "timeoutPolicy": "ALERT_ONLY",
        "timeoutSeconds": 0
    }
    ```
7. Start a new workflow of the type you just created
8. Run your Python file with the `main` method

## C/C++ Support

### C++

1. Export your C++ functions as `extern "C"`:
   * C++ function example (sum two integers)
        ```cpp
        #include <iostream>

        extern "C" int32_t get_sum(const int32_t A, const int32_t B) {
            return A + B; 
        }
        ```
2. Compile and share its library:
   * C++ file name: `simple_cpp_lib.cpp`
   * Library output name goal: `lib.so`
        ```bash
        $ g++ -c -fPIC simple_cpp_lib.cpp -o simple_cpp_lib.o
        $ g++ -shared -Wl,-install_name,lib.so -o lib.so simple_cpp_lib.o
        ```
3. Create a `Task` definition:
    ```json
    {
        "name": "cpp_task_example",
        "description": "C++ Task Example",
        "retryCount": 3,
        "timeoutSeconds": 300,
        "inputKeys": [],
        "outputKeys": [],
        "timeoutPolicy": "TIME_OUT_WF",
        "retryLogic": "FIXED",
        "retryDelaySeconds": 10,
        "responseTimeoutSeconds": 180,
        "inputTemplate": {},
        "rateLimitPerFrequency": 0,
        "rateLimitFrequencyInSeconds": 1,
        "ownerEmail": "example@example.com",
        "backoffScaleFactor": 1
    }
    ```
4. Create a `Workflow` definition:
    ```json
    {
        "name": "workflow_with_cpp_task_example",
        "description": "Workflow with C++ Task example",
        "version": 1,
        "tasks": [
            {
                "name": "cpp_task_example",
                "taskReferenceName": "cpp_task_example_ref_0",
                "inputParameters": {},
                "type": "SIMPLE",
                "decisionCases": {},
                "defaultCase": [],
                "forkTasks": [],
                "startDelay": 0,
                "joinOn": [],
                "optional": false,
                "defaultExclusiveJoinTask": [],
                "asyncComplete": false,
                "loopOver": []
            }
        ],
        "inputParameters": [],
        "outputParameters": {
            "workerOutput": "${cpp_task_example_ref_0.output}"
        },
        "schemaVersion": 2,
        "restartable": true,
        "workflowStatusListenerEnabled": false,
        "ownerEmail": "example@example.com",
        "timeoutPolicy": "ALERT_ONLY",
        "timeoutSeconds": 0,
        "variables": {},
        "inputTemplate": {}
    }
    ```
5. Python Worker example:
    ```python
    from conductor.client.http.models.task import Task
    from conductor.client.http.models.task_result import TaskResult
    from conductor.client.http.models.task_result_status import TaskResultStatus
    from conductor.client.worker.worker_interface import WorkerInterface
    from ctypes import cdll


    class CppWrapper:
        def __init__(self, file_path='./lib.so'):
            self.cpp_lib = cdll.LoadLibrary(file_path)

        def get_sum(self, X: int, Y: int) -> int:
            return self.cpp_lib.get_sum(X, Y)


    class SimpleCppWorker(WorkerInterface):
        cpp_wrapper = CppWrapper()

        def execute(self, task: Task) -> TaskResult:
            execution_result = self.cpp_wrapper.get_sum(1, 2)
            task_result = self.get_task_result_from_task(task)
            task_result.add_output_data(
                'sum', execution_result
            )
            task_result.status = TaskResultStatus.COMPLETED
            return task_result
    ```


## Unit Tests

### Simple validation

```shell
/conductor-python/src$ python3 -m unittest -v
test_execute_task (tst.automator.test_task_runner.TestTaskRunner) ... ok
test_execute_task_with_faulty_execution_worker (tst.automator.test_task_runner.TestTaskRunner) ... ok
test_execute_task_with_invalid_task (tst.automator.test_task_runner.TestTaskRunner) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

### Run with code coverage

```shell
/conductor-python/src$ python3 -m coverage run --source=conductor/ -m unittest
```

Report:

```shell
/conductor-python/src$ python3 -m coverage report
```

Visual coverage results:

```shell
/conductor-python/src$ python3 -m coverage html
```
