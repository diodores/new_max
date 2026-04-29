#my_project/maxbot_rebbit/src/rabbit/consumers/max.py
import asyncio
import json
from src.rabbit.routing import Router


class MaxConsumer:
    def __init__(self, rabbit):
        self.rabbit = rabbit

    async def start(self):
        channel = await self.rabbit.create_channel()

        queue = await channel.declare_queue("max_inbox")

        exchange = self.rabbit.get_exchange()

        await queue.bind(exchange, routing_key="120363423596256859@g.us")
        await queue.bind(exchange, routing_key="whatsapp.chat2")

        async with queue.iterator() as it:
            async for message in it:
                async with message.process():
                    data = json.loads(message.body.decode())

                    if data["routing_key"] == "-72932271489781":
                        print(f"Отправим туда то")


                        print("\n[MAX MESSAGE]")
                        print(json.dumps(data, ensure_ascii=False, indent=2))

                    await asyncio.sleep(1)

