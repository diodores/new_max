from fastapi import APIRouter, Request, HTTPException

from src.models.raw import RawWebhook
from src.models.parser import parse_webhook
from src.rabbit.container import container


router = APIRouter()


ALLOWED_EVENTS = {
    "incomingMessageReceived",
}


@router.post("/{source}")
async def webhook(request: Request, source: str):
    data = await request.json()

    print("\n[RAW]")
    print(data)

    event = data.get("typeWebhook")

    # --- фильтр по типу события ---
    if event not in ALLOWED_EVENTS:
        print("[SKIP EVENT]", event)
        print("*************")
        return {"ignored": True}

    # --- фильтр на мусорные payload ---
    if "messageData" not in data:
        print("[SKIP NO messageData]")
        return {"ignored": True}

    # --- парсинг ---
    try:
        raw = RawWebhook(**data)
    except Exception as e:
        print("[VALIDATION ERROR]", e)
        return {"ignored": True}

    msg = parse_webhook(raw, platform=source)

    print("\n[NORMALIZED]")
    print(msg)
    print(msg.routing_key)
    print("--- STOP!!!! ---")

    # --- проверка producer ---
    producer = container.producer
    if not producer:
        raise HTTPException(status_code=500, detail="Producer not initialized")

    # --- проверка routing ---
    if not msg.routing_key:
        print("[ERROR] empty routing_key")
        return {"ignored": True}

    # --- publish ---
    await producer.publish(
        routing_key=msg.routing_key,
        payload=msg.model_dump()
    )

    return {"ok": True}