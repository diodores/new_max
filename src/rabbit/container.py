#/home/deb/my_project/maxbot_rebbit/src/rabbit/container.py
from src.rabbit.connection import RabbitMQ
from src.rabbit.producer import Producer
from src.rabbit.consumers.whatsapp import WhatsAppConsumer
from src.rabbit.consumers.max import MaxConsumer
from src.config import settings
from src.senders.whatsapp import WhatsAppSender
from src.senders.max import MaxSender

from src.logging_app import log_state, logger
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

            self.producer = Producer(self.rabbit)

        except Exception as e:
            logger.error("container_rabbit_init_failed error=%s", e, exc_info=True)
            raise RabbitConnectionError(str(e))

        try:
            self.whatsapp_sender = WhatsAppSender(settings)
            self.max_sender = MaxSender(settings)

        except Exception as e:
            logger.error("container_senders_init_failed error=%s", e, exc_info=True)
            raise

        try:
            self.whatsapp = WhatsAppConsumer(self.rabbit, self.max_sender)
            self.max = MaxConsumer(self.rabbit, self.whatsapp_sender)

        except Exception as e:
            logger.error("container_consumers_init_failed error=%s", e, exc_info=True)
            raise

        log_state("CONTAINER_READY")

    async def shutdown(self):
        log_state("CONTAINER_SHUTDOWN")

        try:
            await self.rabbit.close()
        except Exception as e:
            logger.error("rabbit_shutdown_error error=%s", e, exc_info=True)

        if self.whatsapp_sender:
            await self.whatsapp_sender.close()

        if self.max_sender:
            await self.max_sender.close()

        log_state("CONTAINER_STOPPED")


container = Container()



