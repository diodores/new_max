#my_project/maxbot_rebbit/src/rabbit/connection.py
import asyncio
import aio_pika

from src.exceptions import RabbitConnectionError, RabbitChannelError, ExchangeNotInitializedError
from src.logging import logger, log_state


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
        log_state("RABBITMQ CONNECTING")
        for attempt in range(10):
            try:
                self._connection = await aio_pika.connect_robust(self._url)
                log_state("RABBIT_CONNECTED", attempt=attempt + 1)
                return
            except Exception as e:
                logger.warning("rabbit_connect_retry attempt=%s error=%s", attempt + 1, e)
                await asyncio.sleep(2)

        log_state("RABBIT_CONNECTION_FAILED")
        logger.error("RABBIT_CONNECTION_FAILED")
        raise RabbitConnectionError ("Не удалось подключится к RabbitMQ, попытки исчерпаны")

    async def close(self):
        """
        Корректное закрытие соединения.
        """
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._exchange = None

            log_state("RABBIT_DISCONNECTED")

    async def create_channel(self):
        """
        Создание канала с QoS.
        """
        if not self._connection:
            log_state("RABBIT_CHANNEL_ERROR", reason="no_connection")
            raise RabbitChannelError("RabbitMQ no_connection")

        try:
            channel = await self._connection.channel(publisher_confirms=True)
            await channel.set_qos(prefetch_count=1)
            log_state("RABBIT_CHANNEL_CREATED")
            return channel
        except Exception as e:
            logger.error("rabbit_channel_error error=%s", e)
            raise RabbitChannelError(str(e))

    async def setup_exchange(self):
        """
        Создание exchange (idempotent по смыслу).
        """
        channel = await self.create_channel()
        log_state("RABBIT_EXCHANGE_READY")

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
            log_state("ERROR", reason="exchange_not_initialized")
            logger.error("ERROR", reason="exchange_not_initialized")
            raise ExchangeNotInitializedError("Exchange not initialized")
        return self._exchange

    async def init(self):
        """
        Удобный единый вход для старта Rabbit слоя.
        """
        await self.connect()
        await self.setup_exchange()

        log_state("RABBIT_INIT_DONE")