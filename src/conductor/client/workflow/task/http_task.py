from __future__ import annotations
from conductor.client.workflow.task.http_input import HttpInput
from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from enum import Enum
from typing import Any, Dict, List


class HttpTask(TaskInterface):
    def __init__(self, task_ref_name: str, http_input: HttpInput) -> HttpTask:
        super().__init__(task_ref_name, TaskType.HTTP)
        self._input_parameters = {
            "http_request": http_input
        }


class HttpMethod(str, Enum):
    GET = "GET",
    PUT = "PUT",
    POST = "POST",
    DELETE = "DELETE",
    HEAD = "HEAD",
    OPTIONS = "OPTIONS"


class HttpInput:
    _method: HttpMethod
    _uri: str
    _headers: Dict[str, List[str]]
    _accept: str
    _content_type: str
    _connection_time_out: int
    _read_timeout: int
    _body: Any

    # TODO add json serializer for param names

    def __init__(self,
                 method: HttpMethod = HttpMethod.GET,
                 uri: str = None,
                 headers: Dict[str, List[str]] = None,
                 accept: str = None,
                 content_type: str = None,
                 connection_time_out: int = None,
                 read_timeout: int = None,
                 body: Any = None) -> HttpInput:
        self._method = method
        self._method = method
        self._uri = uri
        self._headers = headers
        self._accept = accept
        self._content_type = content_type
        self._connection_time_out = connection_time_out
        self._read_timeout = read_timeout
        self._body = body
