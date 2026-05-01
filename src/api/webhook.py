#maxbot_rebbit/src/api/webhook.py
from pathlib import Path

from fastapi import APIRouter, Request, HTTPException

from src.models.raw import RawWebhook
from src.models.parser import parse_webhook
from src.rabbit.container import container
from src.rabbit.routing import Router


router = APIRouter()


ALLOWED_EVENTS = {
    "incomingMessageReceived",
}

path_json = Path(__file__).parent.parent / "routing.json"
router_obj = Router(path_json)

@router.post("/{source}")
async def webhook(request: Request, source: str):
    data = await request.json()
    #print(f"\n{data}")
    event = data.get("typeWebhook")
    #print(f"[RAW] event={event}")

    # --- фильтр по типу события ---
    if event not in ALLOWED_EVENTS:
        #print("[SKIP EVENT]", event)
        #print("*************")
        return {"ignored": True}

    # --- фильтр на мусорные payload ---
    if "messageData" not in data:
        #print("[SKIP NO messageData]")
        return {"ignored": True}

    # --- парсинг ---
    try:
        raw = RawWebhook(**data)
    except Exception as e:
        #print("[VALIDATION ERROR]", e)
        return {"ignored": True}

    msg = parse_webhook(raw, platform=source)

    #print("\n[NORMALIZED]")
    #print(msg)
    #print("---передаю продюсеру---")

    # --- проверка producer ---
    producer = container.producer
    if not producer:
        raise HTTPException(status_code=500, detail="Producer not initialized")

    # --- routing ---
    route = router_obj.resolve(msg.platform, msg.chat_id)

    if not route:
        #print(f"[NO ROUTE] {msg.platform}:{msg.chat_id}")
        return {"ignored": True}

    # --- publish ---
    await producer.publish(
        routing_key=route["chat_id"],
        payload=msg.model_dump()
    )

    return {"ok": True}


