#my_project/maxbot_rebbit/src/models/raw.py
from pydantic import BaseModel
from typing import Dict, Any


class RawWebhook(BaseModel):
    typeWebhook: str
    instanceData: Dict[str, Any]
    timestamp: int
    idMessage: str

    senderData: Dict[str, Any]
    messageData: Dict[str, Any] | None