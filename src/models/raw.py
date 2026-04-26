from pydantic import BaseModel
from typing import Optional, Dict, Any


class RawWebhook(BaseModel):
    typeWebhook: str
    instanceData: Dict[str, Any]
    timestamp: int
    idMessage: str

    senderData: Dict[str, Any]
    messageData: Optional[Dict[str, Any]] = None