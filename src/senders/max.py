import aiohttp
import asyncio
from src.senders.base import BaseSender
from src.config import Settings


class MaxSender(BaseSender):
    def __init__(self, settings: Settings):
        super().__init__(settings)

        self.instance_id = settings.INSTANCE_ID_MAX
        self.token = settings.TOKEN_MAX
        self.base_url = settings.URL_MAX_API

        self.session: aiohttp.ClientSession | None = None

    def _url(self, method: str) -> str:
        return f"{self.base_url}/waInstance{self.instance_id}/{method}/{self.token}"

    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def send_text(self, chat_id: str, text: str) -> dict:
        session = await self._get_session()

        url = self._url("sendMessage")

        payload = {
            "chatId": chat_id,
            "message": text,
        }

        async with session.post(url, json=payload) as resp:
            return await resp.json()

    async def send_file(
        self,
        chat_id: str,
        file_url: str,
        caption: str | None = None
    ) -> dict:
        session = await self._get_session()

        url = self._url("sendFileByUrl")

        # у MAX реально часто пустой payload + query достаточно
        payload = {
            "chatId": chat_id,
            "urlFile": file_url,
            "fileName": file_url.split("/")[-1],
            "caption": caption or "",
        }

        async with session.post(url, json=payload) as resp:
            return await resp.json()

    async def close(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None


# if __name__ == "__main__":
#     async def main():
#         settings = Settings()
#         sender = MaxSender(settings)
#         await sender.send_text(chat_id="-73294784463605", text="test")
#         await sender.close()
#
#     asyncio.run(main())