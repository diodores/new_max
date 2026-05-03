#maxbot_rebbit/src/api/webhook.py
from pathlib import Path

from fastapi import APIRouter, Request, HTTPException
from pydantic import ValidationError

from src.models.raw import RawWebhook
from src.models.parser import parse_webhook
from src.rabbit.container import container
from src.rabbit.routing import Router
from src.api.response import success, ignored
from src.exceptions import WebhookValidationError, ProducerNotReadyError
from src.logging import log_state, logger

router = APIRouter()


ALLOWED_EVENTS = {
    "incomingMessageReceived",
}

path_json = Path(__file__).parent.parent / "routing.json"
router_obj = Router(path_json)

@router.post("/{source}")
async def webhook(request: Request, source: str):
    data = await request.json()
    event = data.get("typeWebhook")

    log_state("RECEIVED", source=source, event=event)

    # --- фильтр по типу события ---
    if event not in ALLOWED_EVENTS:
        log_state("IGNORED", reason="bad_event", event=event, source=source)
        return ignored()

    # --- фильтр на мусорные payload ---
    if "messageData" not in data:
        log_state("IGNORED", reason="no_messageData", source=source)
        return ignored()

    # --- парсинг ---
    try:
        raw = RawWebhook(**data)
    except ValidationError as e:
        log_state("ERROR_VALIDATION", source=source)
        logger.error("validation_error source=%s , error=%s", source, e)
        raise WebhookValidationError(str(e))


    msg = parse_webhook(raw, platform=source)
    log_state("PARSED", chat_id=msg.chat_id, platform=msg.platform)

    # --- проверка producer ---
    producer = container.producer
    if not producer:
        log_state("ERROR", reason="producer_not_ready")
        logger.error("producer_not_ready")
        raise ProducerNotReadyError()

    # --- routing ---
    route = router_obj.resolve(msg.platform, msg.chat_id)

    if not route:
        log_state("IGNORED", reason="no_route", chat_id=msg.chat_id, platform=msg.platform)
        return ignored()

    # --- publish ---
    await producer.publish(
        routing_key=route["chat_id"],
        payload=msg.model_dump()
    )

    return success()


