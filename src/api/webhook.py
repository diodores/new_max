from fastapi import APIRouter, Request
from src.models.raw import RawWebhook
from src.models.parser import parse_webhook
from src.rabbit.container import container
from fastapi import HTTPException


router = APIRouter()


ALLOWED_EVENTS = {
    "incomingMessageReceived",
    "outgoingMessageReceived",
}



@router.post("/{source}")
async def webhook(request: Request, source: str):
    data = await request.json()
    print(data)

    event = data.get("typeWebhook")

    if event not in ALLOWED_EVENTS:
        print(event)
        print("*************")
        return {"ignored": True}

    raw = RawWebhook(**data)

    msg = parse_webhook(raw, platform=source)
    print(msg.routing_key)
    print("--- STOP!!!! ---")


    producer = container.producer
    if not producer:
        raise HTTPException(status_code=500, detail="Producer not initialized")

    await producer.publish(msg.routing_key, msg.model_dump())

    return {"ok": True}


