# Worker

Considering real use cases, the goal is to run multiple workers in parallel. Due to some limitations with Python, a multiprocessing architecture was chosen in order to enable real parallelization.

You can write your workers independently and append them to a list. The `TaskHandler` class will spawn a unique and independent process for each worker, making sure it will behave as expected, by running an infinite loop like this:
* Poll for a `Task` at Conductor Server
* Generate `TaskResult` from given `Task`
* Update given `Task` with `TaskResult` at Conductor Server

## Write workers

Currently, there are three ways of writing a Python worker:
1. [Worker as a function](#worker-as-a-function)
2. [Worker as a class](#worker-as-a-class)
3. [Worker as an annotation](#worker-as-an-annotation)


### Worker as a function

The function should follow this signature:

```python
ExecuteTaskFunction = Callable[
    [
        Union[Task, object]
    ],
    Union[TaskResult, object]
]
```

In other words:
* Input must be either a `Task` or an `object`
    * If it isn't a `Task`, the assumption is - you're expecting to receive the `Task.input_data` as the object
* Output must be either a `TaskResult` or an `object`
    * If it isn't a `TaskResult`, the assumption is - you're expecting to use the object as the `TaskResult.output_data`

Quick example below:

```python
from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus

def execute(task: Task) -> TaskResult:
    task_result = TaskResult(
        task_id=task.task_id,
        workflow_instance_id=task.workflow_instance_id,
        worker_id='your_custom_id'
    )
    task_result.add_output_data('worker_style', 'function')
    task_result.status = TaskResultStatus.COMPLETED
    return task_result
```

In the case you like more details, you can take a look at all possible combinations of workers [here](../../tests/integration/resources/worker/python/python_worker.py)

### Worker as a class

The class must implement `WorkerInterface` class, which requires an `execute` method. The remaining ones are inherited, but can be easily overridden. Example with a custom polling interval:

```python
from conductor.client.http.models import Task, TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.worker_interface import WorkerInterface

class SimplePythonWorker(WorkerInterface):
    def execute(self, task: Task) -> TaskResult:
        task_result = self.get_task_result_from_task(task)
        task_result.add_output_data('worker_style', 'class')
        task_result.add_output_data('secret_number', 1234)
        task_result.add_output_data('is_it_true', False)
        task_result.status = TaskResultStatus.COMPLETED
        return task_result

    def get_polling_interval_in_seconds(self) -> float:
        # poll every 500ms
        return 0.5
```

### Worker as an annotation
A worker can also be invoked by adding a WorkerTask decorator as shown in the below example.
As long as the annotated worker is in any file inside the root folder of your worker application, it will be picked up by the TaskHandler, see [Run Workers](#run-workers)

```python
from conductor.client.worker.worker_task import WorkerTask

@WorkerTask(task_definition_name='python_annotated_task', domain='cool', worker_id='decorated', poll_interval_seconds=1.0)
def python_annotated_task(input) -> object:
    return {'message': 'python is so cool :)'}
```

## Run Workers

Now you can run your workers by calling a `TaskHandler`, example:

```python
from conductor.client.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.configuration.configuration import Configuration
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.worker.worker import Worker

#### Add these lines if running on a mac####
from multiprocessing import set_start_method
set_start_method('fork')
############################################

SERVER_API_URL = 'http://localhost:8080/api'
KEY_ID = '<KEY_ID>'
KEY_SECRET = '<KEY_SECRET>'

configuration = Configuration(
    server_api_url=SERVER_API_URL,
    debug=True,
    authentication_settings=AuthenticationSettings(
        key_id=KEY_ID,
        key_secret=KEY_SECRET
    ),
)

workers = [
    SimplePythonWorker(
        task_definition_name='python_task_example'
    ),
    Worker(
        task_definition_name='python_execute_example',
        execute_function=execute,
        poll_interval=0.25,
    )
]

# If there are decorated workers in your application, scan_for_annotated_workers should be set
# default value of scan_for_annotated_workers is False
with TaskHandler(workers, configuration, scan_for_annotated_workers=True) as task_handler:
    task_handler.start_processes()
    task_handler.join_processes()
```

If you paste the above code in a file called main.py, you can launch the workers by running:
```shell
python3 main.py
```

See [Using Conductor Playground](https://orkes.io/content/docs/getting-started/playground/using-conductor-playground) for more details on how to use Playground environment for testing.

If you're looking for better performance (i.e. more workers of the same type) - you can simply append more instances of the same worker, like this:

```python
workers = [
    SimplePythonWorker(
        task_definition_name='python_task_example'
    ),
    SimplePythonWorker(
        task_definition_name='python_task_example'
    ),
    SimplePythonWorker(
        task_definition_name='python_task_example'
    ),
    ...
]
```

```python
workers = [
    Worker(
        task_definition_name='python_task_example',
        execute_function=execute,
        poll_interval=0.25,
    ),
    Worker(
        task_definition_name='python_task_example',
        execute_function=execute,
        poll_interval=0.25,
    ),
    Worker(
        task_definition_name='python_task_example',
        execute_function=execute,
        poll_interval=0.25,
    )
    ...
]
```

## C/C++ Support
Python is great, but at times you need to call into native C/C++ code. 
Here is an example how you can do that with Conductor SDK.

### 1. Export your C++ functions as `extern "C"`:
   * C++ function example (sum two integers)
        ```cpp
        #include <iostream>

        extern "C" int32_t get_sum(const int32_t A, const int32_t B) {
            return A + B; 
        }
        ```
### 2. Compile and share its library:
   * C++ file name: `simple_cpp_lib.cpp`
   * Library output name goal: `lib.so`
        ```shell
        g++ -c -fPIC simple_cpp_lib.cpp -o simple_cpp_lib.o
        g++ -shared -Wl,-install_name,lib.so -o lib.so simple_cpp_lib.o
        ```
     
### 3. Use the C++ library in your python worker
You can use the Python library to call native code written in C++.  Here is an example that calls native C++ library
from the Python worker.
See [simple_cpp_lib.cpp](src/example/worker/cpp/simple_cpp_lib.cpp) 
and [simple_cpp_worker.py](src/example/worker/cpp/simple_cpp_worker.py) for complete working example.

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

### Next: [Create workflows using Code](../workflow/README.md)
