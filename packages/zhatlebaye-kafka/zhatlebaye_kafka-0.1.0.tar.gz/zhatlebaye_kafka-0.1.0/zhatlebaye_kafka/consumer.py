import json

from aiokafka import AIOKafkaConsumer
from loguru import logger

from router import KafkaRouter


class KafkaConsumer:
    def __init__(self, group_id: str, bootstrap_servers: str, router: KafkaRouter):
        self.bootstrap_servers = bootstrap_servers
        self.router = router
        self.group_id = group_id
        self.consumer = None
        self.shutdown_flag = False

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            *self.router.get_topics(),
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        )
        await self.consumer.start()

    async def stop(self):
        self.shutdown_flag = True

    async def run(self):
        await self.start()
        try:
            while not self.shutdown_flag:
                try:
                    message = await self.consumer.getone()
                    if message is None:
                        continue
                    await self.router.handle_message(message)
                    await self.consumer.commit()
                except Exception as e:
                    logger.error('Error while processing message', error=e)
        finally:
            await self.consumer.stop()
