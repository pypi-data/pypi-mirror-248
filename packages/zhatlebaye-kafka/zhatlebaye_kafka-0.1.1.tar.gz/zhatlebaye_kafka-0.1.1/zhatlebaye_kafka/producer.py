import asyncio
import json

from aiokafka import AIOKafkaProducer
from loguru import logger


class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self._producer = None

    async def __aenter__(self):
        try:
            await self.connect()
        except Exception as e:
            logger.error('Error while starting Kafka producer', error=e)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        try:
            await self.disconnect()
        except Exception as e:
            logger.error('Error while stopping Kafka producer', error=e)

    async def connect(self):
        if self._producer is None:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            await self._producer.start()

            logger.info('Kafka producer started')

    async def disconnect(self):
        if self._producer is not None:
            await self._producer.stop()

    async def send_message(self, topic, message, callback=None):
        try:
            serialized_message = self._serialize_message(message)
            if callback:
                result = await self._producer.send(topic, serialized_message)
                await callback(result)
            else:
                await self._producer.send_and_wait(topic, serialized_message)
        except Exception as e:
            logger.error('Error while sending message to Kafka', error=e, payload=message)

    def send_message_sync(self, topic, message):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_message(topic, message))

    @staticmethod
    def _serialize_message(self, message):
        return json.dumps(message).encode()
