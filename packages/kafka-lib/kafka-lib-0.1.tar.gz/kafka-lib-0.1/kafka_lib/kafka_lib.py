import json
import asyncio
from kafka_lib.producer import Producer
import confluent_kafka as _a

class KafkaLibrary:
    def __init__(self, producer_conf, consumer_conf, consumer_conf1):
        self.producer = Producer(producer_conf)
        self.consumer_conf = consumer_conf
        self.consumer_conf1 = consumer_conf1

    async def consume(self, topic):
        if topic == "topic1":
            consumer = _a.Consumer(self.consumer_conf)
        elif topic == "topic2":
            consumer = _a.Consumer(self.consumer_conf1)
        else:
            raise ValueError("Invalid topic")

        consumer.subscribe([topic])

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == _a.KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"Consumer error: {msg.error()}")
                        break
                msg_value = msg.value().decode('utf-8')
                if msg_value:
                    yield msg_value
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    async def produce(self, topic, data: dict):
        try:
            data = json.dumps(data).encode('utf-8')
            await self.producer.send_async(topic, data)
        except Exception as e:
            print(f"Failed to publish message to Kafka: {e}")