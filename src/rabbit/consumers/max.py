#my_project/maxbot_rebbit/src/rabbit/consumers/max.py
import asyncio
import json

from src.senders.utils import build_message


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

                    msg = build_message(data)

                    if not msg:
                        continue

                    routing_key = str(message.routing_key)

                    if msg["type"] == "text":
                        await self.whatsapp_sender.send_text(
                            chat_id=routing_key,
                            text=msg["text"]
                        )

                    elif msg["type"] == "file":
                        await self.whatsapp_sender.send_file(
                            chat_id=routing_key,
                            file_url=msg["file_url"],
                            caption=msg.get("caption")
                        )

                    print("\n[MAX MESSAGE]")
                    print(f"routing_key: {routing_key}")
                    print(msg)

                    await asyncio.sleep(1)