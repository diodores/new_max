#my_project/maxbot_rebbit/src/rabbit/consumers/whatsapp.py
import asyncio
import json

from src.senders.utils import build_message


class WhatsAppConsumer:
    def __init__(self, rabbit, max_sender):
        self.rabbit = rabbit
        self.max_sender = max_sender

    async def start(self):
        channel = await self.rabbit.create_channel()

        queue = await channel.declare_queue("wa_inbox")

        exchange = self.rabbit.get_exchange()

        await queue.bind(exchange, routing_key="-72932271489781")
        await queue.bind(exchange, routing_key="-73294784463605")

        async with queue.iterator() as it:
            async for message in it:
                async with message.process():
                    data = json.loads(message.body.decode())

                    msg = build_message(data)

                    if not msg:
                        continue

                    routing_key = str(message.routing_key)

                    if msg["type"] == "text":
                        await self.max_sender.send_text(
                            chat_id=routing_key,
                            text=msg["text"]
                        )

                    elif msg["type"] == "file":
                        await self.max_sender.send_file(
                            chat_id=routing_key,
                            file_url=msg["file_url"],
                            caption=msg.get("caption")
                        )

                    print("\n[WHATSAPP MESSAGE]")
                    print(f"routing_key: {routing_key}")
                    print(msg)

                    await asyncio.sleep(1)
