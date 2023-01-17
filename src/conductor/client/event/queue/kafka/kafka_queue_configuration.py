from queue_configuration import QueueConfiguration


class KafkaQueueConfiguration(QueueConfiguration):
    def __init__(self, queue_topic_name: str):
        super(queue_topic_name, 'kafka')
