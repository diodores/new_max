#my_project/maxbot_rebbit/src/rabbit/producer.py
import json
import uuid
from aio_pika import Message


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
        print(f"[PUBLISH] routing_key={routing_key}")
        await exchange.publish(message, routing_key=routing_key)

