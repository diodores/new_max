from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseSender(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def send_text(self, chat_id: str, text: str) -> dict:
        pass

    @abstractmethod
    async def send_file(self, chat_id: str, file_url: str, caption: str | None = None) -> dict:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass