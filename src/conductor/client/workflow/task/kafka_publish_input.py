from typing import Any, Dict
from typing_extensions import Self


class KafkaPublishInput:
    _bootstrap_servers: str
    _key: str
    _key_serializer: str
    _value: str
    _request_timeout_ms: str
    _max_block_ms: str
    _headers: Dict[str, Any]
    _topic: str

    # TODO add json serializer param names

    def __init__(self,
                 bootstrap_servers: str = None,
                 key: str = None,
                 key_serializer: str = None,
                 value: str = None,
                 request_timeout_ms: str = None,
                 max_block_ms: str = None,
                 headers: Dict[str, Any] = None,
                 topic: str = None) -> Self:
        self._bootstrap_servers = bootstrap_servers
        self._key = key
        self._key_serializer = key_serializer
        self._value = value
        self._request_timeout_ms = request_timeout_ms
        self._max_block_ms = max_block_ms
        self. _headers = headers
        self._topic = topic
