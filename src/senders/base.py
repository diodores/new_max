from abc import ABC, abstractmethod
from src.config import Settings


class BaseSender(ABC):
    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    async def send_text(self, chat_id: str, text: str) -> dict:
        pass

    @abstractmethod
    async def send_file(self, chat_id: str, file_url: str, caption: str | None = None) -> dict:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass