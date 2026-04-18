# producer.py
from aio_pika import Message


class Producer:
    def __init__(self, rabbit):
        self.rabbit = rabbit

    async def publish(self, routing_key: str, text: str):
        exchange = self.rabbit.get_exchange()

        await exchange.publish(
            Message(text.encode(), delivery_mode=2),
            routing_key=routing_key,
            mandatory=True
        )