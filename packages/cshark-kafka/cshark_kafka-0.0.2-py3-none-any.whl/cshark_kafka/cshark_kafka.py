import json

from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
from kafka.producer.future import RecordMetadata


class CSharkKafkaProducer:
    topic_name = None
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda m: json.dumps(m, default=str, ensure_ascii=False).encode('utf-8')
    )

    def __init__(self, topic_name: str):
        self.topic_name = topic_name

    def send_sync(self, message: dict):
        try:
            record_metadata = self.producer.send(self.topic_name, key=b'sync_msg', value=message).get(timeout=10)

            return record_metadata
        except KafkaError:
            return 'Error'

    def send_async(self, message: dict):
        self.producer.send(self.topic_name, key=b'async_msg', value=message)

        self.producer.flush()

    def send_async_with_callback(self, message: dict):
        def on_send_success(record_metadata: RecordMetadata):
            print({'status': 'success', 'data': record_metadata})

        def on_send_error(e):
            print({'status': 'failure', 'error': e})

        self.producer.send(self.topic_name, key=b'async_msg_with_callback', value=message).add_callback(on_send_success).add_errback(on_send_error)
        self.producer.flush()


class CSharkKafkaConsumer:
    topic_name = None
    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True,
        consumer_timeout_ms=1000
    )

    def __init__(self, topic_name: str):
        self.topic_name = topic_name

    def consume_from_offset(self, partition_number: int, offset: int):
        partition = TopicPartition(self.topic_name, partition_number)
        self.consumer.assign([partition])
        self.consumer.seek(partition, offset)

        return self.consumer
