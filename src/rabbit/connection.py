#my_project/maxbot_rebbit/src/rabbit/connection.py
import aio_pika


class RabbitMQ:
    def __init__(self, url: str):
        self._url = url
        self._connection = None
        self._exchange = None

    async def connect(self):
        self._connection = await aio_pika.connect_robust(self._url)

    async def close(self):
        if self._connection:
            await self._connection.close()

    async def create_channel(self):
        channel = await self._connection.channel(publisher_confirms=True)
        await channel.set_qos(prefetch_count=1)
        return channel

    async def setup_exchange(self):
        channel = await self.create_channel()
        self._exchange = await channel.declare_exchange(
            "messenger_exchange",
            aio_pika.ExchangeType.DIRECT,
            durable=True,
        )

    def get_exchange(self):
        return self._exchange

