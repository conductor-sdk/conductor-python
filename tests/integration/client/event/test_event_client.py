from conductor.client.event.queue.kafka_queue_configuration import KafkaConsumerConfiguration
from conductor.client.event.queue.kafka_queue_configuration import KafkaProducerConfiguration
from conductor.client.event.queue.kafka_queue_configuration import KafkaQueueConfiguration
from conductor.client.http.api_client import ApiClient
from conductor.client.event.event_client import EventClient


def test_kafka_queue_configuration(api_client: ApiClient):
    kafka_configuration = create_kafka_queue_configuration()
    event_client = EventClient(api_client)
    delete_response = event_client.delete_queue_configuration(
        kafka_configuration
    )
    event_client.put_queue_configuration(kafka_configuration)
    received_queue_configuration = event_client.get_kafka_queue_configuration(
        'test_sdk_kafka_queue_name'
    )
    expected_queue = kafka_configuration.get_worker_configuration()
    assert received_queue_configuration == expected_queue
    event_client.delete_queue_configuration(kafka_configuration)


def create_kafka_queue_configuration() -> KafkaQueueConfiguration:
    kafka_queue_configuration = KafkaQueueConfiguration(
        'test_sdk_kafka_queue_name'
    )
    kafka_queue_configuration.add_consumer(
        KafkaConsumerConfiguration('localhost:9092')
    )
    kafka_queue_configuration.add_producer(
        KafkaProducerConfiguration('localhost:9092')
    )
    return kafka_queue_configuration
