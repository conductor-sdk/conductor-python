import datetime
from dataclasses import dataclass
from random import random

from conductor.client.http.models import TaskResult, Task
from conductor.client.http.models.task_result_status import TaskResultStatus
from conductor.client.worker.exception import NonRetryableException
from conductor.client.worker.worker_task import worker_task


class UserDetails:
    """
    User info data class with constructor to set properties
    """

    swagger_types = {
        '_name': 'str',
        '_user_id': 'str',
        '_addresses': 'object',
    }

    attribute_map = {
        '_name': 'name',
        '_user_id': 'user_id',
        '_addresses': 'addresses'
    }

    def __init__(self, name: str, user_id: int, addresses: list[object]) -> None:
        self._name = name
        self._user_id = user_id
        self._addresses = addresses

    @property
    def name(self) -> str:
        return self._name

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def address(self) -> list[object]:
        return self._addresses


@dataclass
class OrderInfo:
    """
    Python data class that uses dataclass
    """
    order_id: int
    sku: str
    quantity: int
    sku_price: float


@worker_task(task_definition_name='get_user_info')
def get_user_info(user_id: str) -> UserDetails:
    return UserDetails(name='user_' + user_id, user_id=user_id, addresses=[{
        'street': '21 jump street',
        'city': 'new york'
    }])


@worker_task(task_definition_name='save_order')
def save_order(order_details: OrderInfo) -> OrderInfo:
    print(f'order_details: {order_details}, type={type(order_details)}')
    order_details.sku_price = order_details.quantity * order_details.sku_price
    return order_details


@worker_task(task_definition_name='process_task')
def process_task(task: Task) -> TaskResult:
    task_result = task.to_task_result(TaskResultStatus.COMPLETED)
    task_result.add_output_data('name', 'orkes')
    task_result.add_output_data('complex', UserDetails(name='u1', addresses=[], user_id=5))
    task_result.add_output_data('time', datetime.datetime.now())
    return task_result


@worker_task(task_definition_name='failure')
def always_fail() -> dict:
    # raising NonRetryableException updates the task with FAILED_WITH_TERMINAL_ERROR status
    raise NonRetryableException('this worker task will always have a terminal failure')


@worker_task(task_definition_name='fail_but_retry')
def fail_but_retry() -> int:
    numx = random.randint(0, 10)
    if numx < 8:
        # raising NonRetryableException updates the task with FAILED_WITH_TERMINAL_ERROR status
        raise Exception(f'number {numx} is less than 4.  I am going to fail this task and retry')
    return numx
