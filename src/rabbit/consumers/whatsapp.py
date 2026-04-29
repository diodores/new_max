#my_project/maxbot_rebbit/src/rabbit/consumers/whatsapp.py
import asyncio
import json


class WhatsAppConsumer:
    def __init__(self, rabbit):
        self.rabbit = rabbit

    async def start(self):
        channel = await self.rabbit.create_channel()

        queue = await channel.declare_queue("wa_inbox")

        exchange = self.rabbit.get_exchange()

        await queue.bind(exchange, routing_key="-72932271489781")
        await queue.bind(exchange, routing_key="max.chat2")

        async with queue.iterator() as it:
            async for message in it:
                async with message.process():
                    data = json.loads(message.body.decode())


                    print("\n[WHATSAPP MESSAGE]")
                    print(json.dumps(data, ensure_ascii=False, indent=2))

                    await asyncio.sleep(1)

