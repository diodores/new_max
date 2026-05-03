#my_project/maxbot_rebbit/src/rabbit/container.py
from src.rabbit.connection import RabbitMQ
from src.rabbit.producer import Producer
from src.rabbit.consumers.whatsapp import WhatsAppConsumer
from src.rabbit.consumers.max import MaxConsumer
from src.config import settings
from src.senders.whatsapp import WhatsAppSender
from src.senders.max import MaxSender
from src.logging import log_state, logger
from src.exceptions import RabbitConnectionError, ProducerNotReadyError


class Container:
    def __init__(self):
        self.rabbit = None
        self.producer = None

        self.whatsapp = None
        self.whatsapp_sender = None

        self.max = None
        self.max_sender = None

    async def init(self):
        log_state("CONTAINER_INIT_START")

        try:
            self.rabbit = RabbitMQ(settings.RABBITMQ_URL)
            await self.rabbit.connect()
            await self.rabbit.setup_exchange()
            log_state("RABBIT_READY")

        except Exception as e:
            logger.error("rabbit_init_failed error=%s", e)
            raise RabbitConnectionError(str(e))

        try:
            self.producer = Producer(self.rabbit)

            if not self.producer:
                raise ProducerNotReadyError("Producer init failed")

            log_state("PRODUCER_READY")

        except Exception as e:
            logger.error("producer_init_failed error=%s", e)
            raise ProducerNotReadyError(str(e))


        # SENDERS
        try:
            self.whatsapp_sender = WhatsAppSender(settings)
            self.max_sender = MaxSender(settings)

            log_state("SENDERS_READY")

        except Exception as e:
            logger.error("senders_init_failed error=%s", e)
            raise


        # CONSUMERS
        try:
            self.whatsapp = WhatsAppConsumer(
                self.rabbit,
                self.max_sender
            )

            self.max = MaxConsumer(
                self.rabbit,
                self.whatsapp_sender
            )

            log_state("CONSUMERS_READY")

        except Exception as e:
            logger.error("consumers_init_failed error=%s", e)
            raise

        log_state("CONTAINER_INIT_DONE")

    async def shutdown(self):
        log_state("CONTAINER_SHUTDOWN_START")

        try:
            await self.rabbit.close()
        except Exception as e:
            logger.error("rabbit_shutdown_failed error=%s", e)

        if self.whatsapp_sender:
            await self.whatsapp_sender.close()

        if self.max_sender:
            await self.max_sender.close()

        log_state("CONTAINER_SHUTDOWN_DONE")

container = Container()


if __name__ == "__main__":

    ...
    # import asyncio
    #
    #
    # async def main():
    #     container = Container()
    #
    #     await container.init()
    #
    #     await container.producer.publish(
    #         "max.chat1",
    #         "Сообщение для чата макса"
    #     )
    #
    #     await asyncio.sleep(30)
    #
    #     await asyncio.gather(
    #         container.whatsapp.start(),
    #         container.max.start()
    #     )
    #
    #
    # asyncio.run(main())