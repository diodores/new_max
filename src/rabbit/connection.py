#/home/deb/my_project/maxbot_rebbit/src/rabbit/connection.py
import asyncio
import aio_pika

from src.exceptions import (
    RabbitConnectionError,
    RabbitChannelError,
    ExchangeNotInitializedError
)

from src.logging_app import logger, log_state


class RabbitMQ:
    def __init__(self, url: str):
        self._url = url
        self._connection = None
        self._exchange = None

    async def connect(self):
        log_state("RABBIT_CONNECTING")

        for attempt in range(10):
            try:
                self._connection = await aio_pika.connect_robust(self._url)

                log_state("RABBIT_CONNECTED")
                return

            except Exception as e:
                logger.warning(
                    "rabbit_connect_retry attempt=%s error=%s",
                    attempt + 1,
                    e
                )
                await asyncio.sleep(2)

        logger.error("rabbit_connection_failed", exc_info=True)
        raise RabbitConnectionError("Rabbit connection failed")

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._exchange = None

            log_state("RABBIT_DISCONNECTED")

    async def create_channel(self):
        if not self._connection:
            raise RabbitChannelError("no connection")

        try:
            channel = await self._connection.channel(publisher_confirms=True)
            await channel.set_qos(prefetch_count=1)
            return channel

        except Exception as e:
            logger.error("rabbit_channel_error error=%s", e, exc_info=True)
            raise RabbitChannelError(str(e))

    async def setup_exchange(self):
        channel = await self.create_channel()

        self._exchange = await channel.declare_exchange(
            "messenger_exchange",
            aio_pika.ExchangeType.DIRECT,
            durable=True,
        )

        log_state("RABBIT_READY")

    def get_exchange(self):
        if not self._exchange:
            raise ExchangeNotInitializedError()

        return self._exchange

    async def init(self):
        await self.connect()
        await self.setup_exchange()

        log_state("RABBIT_INIT_DONE")

