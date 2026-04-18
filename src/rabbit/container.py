# container.py
from src.rabbit.connection import RabbitMQ
from src.rabbit.producer import Producer
from src.rabbit.consumers.whatsapp import WhatsAppConsumer
from src.rabbit.consumers.max import MaxConsumer
from src.config import settings


class Container:
    def __init__(self):
        self.rabbit = None
        self.producer = None

        self.whatsapp = None
        self.max = None

    async def init(self):
        self.rabbit = RabbitMQ(settings.RABBITMQ_URL)
        await self.rabbit.connect()

        await self.rabbit.setup_exchange()

        self.producer = Producer(self.rabbit)

        self.whatsapp = WhatsAppConsumer(self.rabbit)
        self.max = MaxConsumer(self.rabbit)

    async def shutdown(self):
        await self.rabbit.close()


if __name__ == '__main__':
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