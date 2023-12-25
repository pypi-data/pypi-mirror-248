from loguru import logger


class KafkaRouter:
    def __init__(self):
        self.handlers = {}
        self.topics = set()

    def add_handler(self, topic, handler):
        if not callable(handler):
            raise ValueError('Handler must be callable')
        self.topics.add(topic)
        self.handlers[topic] = handler

    async def handle_message(self, message):
        handler = self.handlers.get(message.topic)
        if handler:
            try:
                await handler(message.value)
            except Exception as e:
                logger.error('Error while handling message', error=e, topic=message.topic)

    def get_topics(self):
        return list(self.topics)
