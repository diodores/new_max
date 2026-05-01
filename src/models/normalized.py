#my_project/maxbot_rebbit/src/models/normalized.py

from typing import Literal
from pydantic import BaseModel


EventType = Literal[
    "incomingMessageReceived",
    "outgoingMessageReceived",
    "deletedMessage",
]


class NormalizedMessage(BaseModel):
    platform: str
    chat_id: str
    chat_name: str
    author: str

    text: str | None = None
    reaction: str | None = None

    media_url: str | None = None
    file_name: str | None = None
    caption: str | None = None

    quoted_text: str | None = None
    quoted_media_url: str | None = None
    quoted_file_name: str | None = None
    quoted_caption: str | None = None

    # ✔ FORWARD SUPPORT
    is_forwarded: bool = False
    forward_score: int = 0

    event: EventType = "incomingMessageReceived"
    timestamp: int = 0
    datetime_msk: str | None = None

    reply_to_message_id: str | None = None
    message_id: str = ""