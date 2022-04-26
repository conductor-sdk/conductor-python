from conductor.client.http.models.task_result import TaskResult
from typing import Callable


class ExternalStorageSettings:
    def __init__(
        self,
        external_storage_handler: Callable[[TaskResult], str],
        task_output_payload_threshold_kb: int = 3072,
        task_output_max_payload_threshold_kb: int = 10240,
    ):
        self.external_storage_handler = external_storage_handler
        self.task_output_payload_threshold_kb = task_output_payload_threshold_kb
        self.task_output_max_payload_threshold_kb = task_output_max_payload_threshold_kb
