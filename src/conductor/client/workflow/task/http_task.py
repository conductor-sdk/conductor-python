from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from copy import deepcopy
from enum import Enum
from typing import Any, Dict, List
from typing_extensions import Self


class HttpMethod(str, Enum):
    GET = "GET",
    PUT = "PUT",
    POST = "POST",
    DELETE = "DELETE",
    HEAD = "HEAD",
    OPTIONS = "OPTIONS"


class HttpInput:
    def __init__(self,
                 method: HttpMethod = HttpMethod.GET,
                 uri: str = None,
                 headers: Dict[str, List[str]] = None,
                 accept: str = None,
                 content_type: str = None,
                 connection_time_out: int = None,
                 read_timeout: int = None,
                 body: Any = None) -> Self:
        self._method = deepcopy(method)
        self._uri = deepcopy(uri)
        self._headers = deepcopy(headers)
        self._accept = deepcopy(accept)
        self._content_type = deepcopy(content_type)
        self._connection_time_out = deepcopy(connection_time_out)
        self._read_timeout = deepcopy(read_timeout)
        self._body = deepcopy(body)


class HttpTask(TaskInterface):
    def __init__(self, task_ref_name: str, http_input: HttpInput) -> Self:
        super().__init__(
            task_reference_name=task_ref_name,
            task_type=TaskType.HTTP,
            input_parameters={
                "http_request": http_input
            }
        )
