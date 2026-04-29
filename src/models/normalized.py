#maxbot_rebbit/src/models/normalized.py
from typing import Literal
from pydantic import BaseModel


EventType = Literal[
    "incomingMessageReceived",
    "outgoingMessageReceived",
    "deletedMessage",
]


class NormalizedMessage(BaseModel):
    platform: str               # max / whatsapp
    chat_id: str
    chat_name: str
    author: str

    text: str | None = None
    media_url: str | None = None
    file_name: str | None = None
    caption: str | None = None

    event: EventType = "incomingMessageReceived"
    timestamp: int = 0
    datetime_msk: str | None = None

    reply_to_message_id: str | None = None

    message_id: str = ""

    # доп. полезно для роутинга в rabbit
    #routing_key: str | None = None

