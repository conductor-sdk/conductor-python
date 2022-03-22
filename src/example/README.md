# Python Worker Examples
This folder contains the examples on how to use Python SDK.

## Install Conductor Python SDK
```shell
python3 -m pip install conductor-python
```

## Example Files
#### main/main.py
Initializes two workers that polls for the tasks by name `task1` and `task2` and starts polling server for work.

#### worker/python/simple_python_worker.py
Minimalistic worker

#### worker/cpp/simple_cpp_worker.py
A Python wrapper that executes C++ code as Conductor worker

## Run Workers against localhost
Execute main/main.py
```shell
conductor-python/src/example> python main/main.py
```

