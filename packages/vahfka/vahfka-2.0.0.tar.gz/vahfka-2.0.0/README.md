vahfka

The vahfka library simplifies Kafka interaction by providing convenient abstractions for both producing and consuming messages. It seamlessly integrates with the kafka-python library and offers additional features for asynchronous message sending and context management.

Installation

You can install the vahfka library using pip:
```bash
pip install vahfka
```

Usage

Initializing the Kafka Producer:
```python
from vahfka import KafkaProducerWithCallbacks
```

# Create a KafkaProducerWithCallbacks instance
```python
kafka_producer = KafkaProducerWithCallbacks(bootstrap_servers='localhost:9092')
```

Sending Messages:

Synchronous Message Sending:
```python
# Send a message synchronously
kafka_producer.send_message(topic='example_topic', message={'key': 'value'})
```

Asynchronous Message Sending:

```python
# Send a message asynchronously
kafka_producer.send_message_async(topic='example_topic', message={'key': 'value'})
Kafka Consumer Wrapper:
from vahfka import KafkaConsumerWrapper

# Create a KafkaConsumerWrapper instance
kafka_consumer = KafkaConsumerWrapper(
    bootstrap_servers='localhost:9092',
    group_id='my-group',
    topics=['example_topic']
)

```

```python
Consuming Messages:
# Consume messages from Kafka topic
messages = kafka_consumer.consume_messages()
print(messages)
```

```python
Context Management:
# Use the KafkaProducerWithCallbacks as a context manager
with KafkaProducerWithCallbacks(bootstrap_servers='localhost:9092') as producer:
    producer.send_message(topic='example_topic', message={'key': 'value'})

```


Example
```python
from vahfka import KafkaProducerWithCallbacks, KafkaConsumerWrapper

# Initialize KafkaProducerWithCallbacks and KafkaConsumerWrapper instances
kafka_producer = KafkaProducerWithCallbacks(bootstrap_servers='localhost:9092')
kafka_consumer = KafkaConsumerWrapper(
    bootstrap_servers='localhost:9092',
    group_id='my-group',
    topics=['example_topic']
)

# Send a message
kafka_producer.send_message(topic='example_topic', message={'key': 'value'})

# Consume messages
messages = kafka_consumer.consume_messages()
print(messages)

```

For questions, issues, or contributions, please visit the https://gitlab.com/magmam/egov