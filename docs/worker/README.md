# Worker

Considering real use cases, the goal is to run multiple workers in parallel. Due to some limitations with Python, a multiprocessing architecture was chosen in order to enable real parallelization.

You should basically write your workers and append them to a list. The `TaskHandler` class will spawn a unique and independent process for each worker, making sure it will behave as expected, by running an infinite loop like this:
* Poll for a `Task` at Conductor Server
* Generate `TaskResult` from given `Task`
* Update given `Task` with `TaskResult` at Conductor Server

## Write workers

Currently, there are two ways of writing a Python worker:
1. [Worker as a function](#worker-as-a-function)
2. [Worker as a class](#worker-as-a-class)


### Worker as a function

The function must receive a `Task` as input and produce `TaskResult` as output, example:

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

### Worker as a class

The class must implement `WorkerInterface` class, which requires `execute` method. The remaining ones are inherited, but can be easily overridden. Example:

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

## Run Workers

Now you can use your workers by calling a `TaskHandler`, example:

```python
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.worker.worker import Worker

workers = [
    SimplePythonWorker(
        task_definition_name='python_task_example'
    ),
    Worker(
        task_definition_name='python_task_example',
        execute_function=execute,
        poll_interval=0.25,
    )
]

with TaskHandler(workers, configuration) as task_handler:
    task_handler.start_processes()
    task_handler.join_processes()
```

```shell
python3 main.py
```

See [Using Conductor Playground](https://orkes.io/content/docs/getting-started/playground/using-conductor-playground) for more details on how to use Playground environment for testing.

Check out more examples, like this general usage: [main.py](../../src/example/main/main.py)


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
