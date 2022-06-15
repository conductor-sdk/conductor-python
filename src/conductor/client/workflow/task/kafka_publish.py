from __future__ import annotations
from conductor.client.workflow.task.task_type import TaskType
from src.conductor.client.workflow.task.http_input import HttpInput
from src.conductor.client.workflow.task.kafka_publish_input import KafkaPublishInput
from task import TaskInterface


class KafkaPublishTask(TaskInterface):
    def __init__(self, task_ref_name: str, kafka_publish_input: KafkaPublishInput = None) -> KafkaPublishTask:
        super().__init__(task_ref_name, TaskType.KAFKA_PUBLISH)
        self._input_parameters = {
            "kafka_request": kafka_publish_input
        }
