#/home/deb/my_project/maxbot_rebbit/src/rabbit/producer.py
import json
import uuid
import asyncio
from aio_pika import Message

from src.exceptions import PublishError
from src.logging_app import log_state, logger




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
            headers={"source": payload.get("platform")},
        )

        log_state(
            "PUBLISH_ATTEMPT",
            routing_key=routing_key,
            message_id=message.message_id
        )

        last_error = None

        for attempt in range(3):
            try:
                await exchange.publish(message, routing_key=routing_key)

                log_state(
                    "PUBLISH_SUCCESS",
                    routing_key=routing_key,
                    attempt=attempt + 1
                )
                return

            except Exception as e:
                last_error = e

                log_state(
                    "PUBLISH_RETRY",
                    routing_key=routing_key,
                    attempt=attempt + 1
                )

                logger.warning(
                    "publish_failed attempt=%s routing_key=%s error=%s",
                    attempt + 1,
                    routing_key,
                    str(e)
                )

                await asyncio.sleep(0.3 * (attempt + 1))

        # ❗ ВАЖНО: финальный блок ВНЕ цикла
        log_state(
            "PUBLISH_FAILED",
            routing_key=routing_key
        )

        logger.error(
            "publish_failed_final routing_key=%s error=%s",
            routing_key,
            str(last_error),
            exc_info=True
        )

        raise PublishError(str(last_error))

