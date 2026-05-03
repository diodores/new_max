#my_project/maxbot_rebbit/src/rabbit/consumers/max.py
import asyncio
import json

from src.senders.utils import build_message
from src.logging import log_state, logger


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

        log_state("MAX_CONSUMER_STARTED")

        async with queue.iterator() as it:
            async for message in it:

                async with message.process():
                    try:
                        data = json.loads(message.body.decode())

                        log_state(
                            "MAX_MESSAGE_RECEIVED",
                            routing_key=message.routing_key
                        )

                        msg = build_message(data)

                        if not msg:
                            log_state(
                                "MAX_MESSAGE_DROPPED",
                                reason="invalid_message",
                                routing_key=message.routing_key
                            )
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

                        log_state(
                            "MAX_MESSAGE_PROCESSED",
                            routing_key=routing_key,
                            type=msg["type"]
                        )

                    except Exception as e:
                        logger.error(
                            "max_consumer_error routing_key=%s error=%s",
                            message.routing_key,
                            e
                        )

                        log_state(
                            "MAX_MESSAGE_ERROR",
                            routing_key=message.routing_key
                        )

                await asyncio.sleep(1)