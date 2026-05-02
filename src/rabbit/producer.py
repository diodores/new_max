#my_project/maxbot_rebbit/src/rabbit/producer.py
import json
import uuid
import asyncio
from aio_pika import Message

from src.exceptions import PublishError


class Producer:
    def __init__(self, rabbit):
        self.rabbit = rabbit

    async def publish(self, routing_key: str, payload: dict):
        exchange = self.rabbit.get_exchange()

        body = json.dumps(payload, ensure_ascii=False).encode()

        message = Message(
            body=body,
            delivery_mode=2,
            content_type="application/json",
            message_id=str(uuid.uuid4()),
            headers={
                "source": payload.get("platform"),
            },
        )

        last_error = None

        for attempt in range(3):
            try:
                await exchange.publish(message, routing_key=routing_key)
                return

            except Exception as e:
                last_error = e
                await asyncio.sleep(0.3 * (attempt + 1))

        raise PublishError(str(last_error))
