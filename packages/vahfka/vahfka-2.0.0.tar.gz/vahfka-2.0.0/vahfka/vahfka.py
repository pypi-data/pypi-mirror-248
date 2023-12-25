from kafka import KafkaProducer, KafkaConsumer
from typing import Dict, Optional, Callable
import json

class KafkaLibrary:
    def __init__(self, bootstrap_servers: str):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def send_message(self, topic: str, message: Dict) -> None:
        json_data = json.dumps(message)
        encoded_data = json_data.encode('utf-8')
        self.producer.send(topic, value=encoded_data)

class KafkaProducerWithCallbacks(KafkaLibrary):
    def __init__(self, bootstrap_servers: str):
        super().__init__(bootstrap_servers)

    def send_message_async(self, topic: str, message: Dict, callback: Optional[Callable] = None) -> None:
        json_data = json.dumps(message)
        encoded_data = json_data.encode('utf-8')
        future = self.producer.send(topic, value=encoded_data)
        if callback:
            future.add_callback(callback)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.producer.close()


class KafkaConsumerWrapper:
    def __init__(self, bootstrap_servers: str, group_id: str, topics: list):
        self.consumer = KafkaConsumer(
            *topics,
            group_id=group_id,
            bootstrap_servers=[bootstrap_servers],
            consumer_timeout_ms=3000,
            value_deserializer=lambda m: json.loads(m.decode('ascii')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

    def consume_messages(self) -> list:
        messages = []
        for message in self.consumer:
            messages.append(message.value)
        return messages

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.consumer.close()