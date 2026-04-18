import asyncio


class WhatsAppConsumer:
    def __init__(self, rabbit):
        self.rabbit = rabbit

    async def start(self):
        channel = await self.rabbit.create_channel()

        queue = await channel.declare_queue("wa_inbox")

        exchange = self.rabbit.get_exchange()

        await queue.bind(exchange, routing_key="max.chat1")
        await queue.bind(exchange, routing_key="max.chat2")

        async with queue.iterator() as it:
            async for message in it:
                async with message.process():
                    print("[WHATSAPP]", message.body.decode())
                    await asyncio.sleep(1)