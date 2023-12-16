import functools

from conductor.client.automator.task_handler import register_decorated_fn
from conductor.client.workflow.task.simple_task import SimpleTask


def WorkerTask(task_definition_name: str, poll_interval: int = 100, domain: str = None, worker_id: str = None):
    def worker_task_func(func):
        register_decorated_fn(name=task_definition_name, poll_interval=poll_interval, domain=domain,
                              worker_id=worker_id, func=func)

        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            if 'task_ref_name' in kwargs:
                task = SimpleTask(task_def_name=task_definition_name, task_reference_name=kwargs['task_ref_name'])
                kwargs.pop('task_ref_name')
                task.input_parameters.update(kwargs)
                return task
            return func(*args, **kwargs)

        return wrapper_func

    return worker_task_func


def worker_task(task_definition_name: str, poll_interval: int = 100, domain: str = None, worker_id: str = None):
    def worker_task_func(func):
        register_decorated_fn(name=task_definition_name, poll_interval=poll_interval, domain=domain,
                              worker_id=worker_id, func=func)

        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            if 'task_ref_name' in kwargs:
                task = SimpleTask(task_def_name=task_definition_name, task_reference_name=kwargs['task_ref_name'])
                kwargs.pop('task_ref_name')
                task.input_parameters.update(kwargs)
                return task
            return func(*args, **kwargs)

        return wrapper_func

    return worker_task_func
