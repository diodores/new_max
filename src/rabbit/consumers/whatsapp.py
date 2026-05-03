import asyncio
import json

from src.senders.utils import build_message
from src.logging import log_state, logger, log_block_end


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

        log_state("WHATSAPP_CONSUMER_STARTED")

        async with queue.iterator() as it:
            async for message in it:

                async with message.process():
                    try:
                        data = json.loads(message.body.decode())

                        msg = build_message(data)
                        if not msg:
                            continue

                        routing_key = str(message.routing_key)

                        # TEXT
                        if msg["type"] == "text":
                            print(msg["text"])
                            await self.max_sender.send_text(
                                chat_id=routing_key,
                                text=msg["text"]
                            )

                        # FILE
                        elif msg["type"] == "file":
                            await self.max_sender.send_file(
                                chat_id=routing_key,
                                file_url=msg["file_url"],
                                caption=msg.get("caption")
                            )

                        log_state(
                            "WA_MESSAGE_SENT",
                            routing_key=routing_key,
                            type=msg["type"]
                        )
                        log_block_end(routing_key)

                    except Exception as e:
                        logger.error(
                            "whatsapp_consumer_error routing_key=%s error=%s",
                            message.routing_key,
                            e
                        )

                        log_state(
                            "WHATSAPP_CONSUMER_ERROR",
                            routing_key=message.routing_key
                        )

                await asyncio.sleep(1)