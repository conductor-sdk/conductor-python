from conductor.client.workflow.task.kafka_publish_input import KafkaPublishInput
from conductor.client.workflow.task.task import TaskInterface
from conductor.client.workflow.task.task_type import TaskType
from typing_extensions import Self


class KafkaPublishTask(TaskInterface):
    def __init__(self, task_ref_name: str, kafka_publish_input: KafkaPublishInput = None) -> Self:
        super().__init__(task_ref_name, TaskType.KAFKA_PUBLISH)
        self._input_parameters = {
            "kafka_request": kafka_publish_input
        }
