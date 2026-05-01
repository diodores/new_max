#my_project/maxbot_rebbit/src/rabbit/connection.py
# my_project/maxbot_rebbit/src/rabbit/connection.py

import asyncio
import aio_pika


class RabbitMQ:
    def __init__(self, url: str):
        self._url = url
        self._connection = None
        self._exchange = None

    async def connect(self):
        """
        Подключение к RabbitMQ с retry,
        чтобы не падать при раннем старте контейнера.
        """
        for attempt in range(10):
            try:
                self._connection = await aio_pika.connect_robust(self._url)
                return
            except Exception as e:
                print(f"[RabbitMQ] not ready ({attempt + 1}/10): {e}")
                await asyncio.sleep(2)

        raise RuntimeError("RabbitMQ connection failed after retries")

    async def close(self):
        """
        Корректное закрытие соединения.
        """
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._exchange = None

    async def create_channel(self):
        """
        Создание канала с QoS.
        """
        if not self._connection:
            raise RuntimeError("RabbitMQ is not connected")

        channel = await self._connection.channel(publisher_confirms=True)
        await channel.set_qos(prefetch_count=1)
        return channel

    async def setup_exchange(self):
        """
        Создание exchange (idempotent по смыслу).
        """
        channel = await self.create_channel()

        self._exchange = await channel.declare_exchange(
            "messenger_exchange",
            aio_pika.ExchangeType.DIRECT,
            durable=True,
        )

    def get_exchange(self):
        """
        Безопасный доступ к exchange.
        """
        if not self._exchange:
            raise RuntimeError("Exchange not initialized. Call setup_exchange() first.")
        return self._exchange

    async def init(self):
        """
        Удобный единый вход для старта Rabbit слоя.
        """
        await self.connect()
        await self.setup_exchange()