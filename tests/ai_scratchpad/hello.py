import functools
from typing import List

from conductor.client.workflow.conductor_workflow import ConductorWorkflow


def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value

        return wrapper_repeat

    return decorator_repeat


def switch(ref: str, condition: str, cases: dict[str, object]):
    print('eval ' + condition)
    return


def worker(name: str, polling_interval: int = 0.1):
    def do_twice(func):
        @functools.wraps(func)
        def wrapper_do_twice(*args, **kwargs):
            # func()
            func()
            print('hello intercepted: ' + str(polling_interval))

        return wrapper_do_twice

    return do_twice


@worker(name='viren', polling_interval=100)
def hello():
    print('Hello world')


def workflow() -> ConductorWorkflow:
    wf = ConductorWorkflow()
    wf >> hello() >> switch() >> hello()
    pass


def main():
    workflow()
    print('Done')


if __name__ == '__main__':
    main()
