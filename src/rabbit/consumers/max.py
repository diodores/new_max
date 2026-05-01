#my_project/maxbot_rebbit/src/rabbit/consumers/max.py
import asyncio
import json



class MaxConsumer:
    def __init__(self, rabbit, whatsapp_sender):
        self.rabbit = rabbit
        self.whatsapp_sender = whatsapp_sender

    async def start(self):
        channel = await self.rabbit.create_channel()

        queue = await channel.declare_queue("max_inbox")

        exchange = self.rabbit.get_exchange()

        await queue.bind(exchange, routing_key="120363423596256859@g.us")
        await queue.bind(exchange, routing_key="120363408049945016@g.us")

        async with queue.iterator() as it:
            async for message in it:
                async with message.process():
                    data = json.loads(message.body.decode())
                    data= str(data)
                    routing_key = message.routing_key

                    await self.whatsapp_sender.send_text(chat_id=routing_key, text=data)

                    print("\n[MAX MESSAGE]")
                    print(f"routing_key: {routing_key}")
                    print(json.dumps(data, ensure_ascii=False, indent=2))

                    await asyncio.sleep(1)



