import asyncio
import json
from typing import Callable
import confluent_kafka as _a

class Producer:
    def __init__(self, producer_conf):
        self.producer = _a.Producer(producer_conf)

    def send_sync(self, topic, data: bytes):
        self.producer.produce(topic, value=data)
        self.producer.flush()

    async def send_async(self, topic, data: bytes):
        return await asyncio.to_thread(self.send_sync, topic, data)

    async def send_async_with_callback(self, topic, data: bytes, callback: Callable):
        def delivery_report(err, msg):
            if err is not None:
                print(f'Message delivery failed: {err}')
            else:
                print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

            callback(err, msg)

        self.producer.produce(topic, value=data, callback=delivery_report)
        self.producer.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.producer.flush()

