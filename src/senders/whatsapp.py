import asyncio

import aiohttp
from src.senders.base import BaseSender
from src.config import Settings


class WhatsAppSender(BaseSender):
    def __init__(self, settings: Settings):
        super().__init__(settings)

        self.instance_id = settings.INSTANCE_ID_WHATSAPP
        self.token = settings.TOKEN_WHATSAPP
        self.base_url = settings.URL_MAX_WHATSAPP
        self.media_url = settings.URL_MAX_WHATSAPP_MEDIA

        self.session: aiohttp.ClientSession | None = None

    def _url(self, method: str) -> str:
        return f"{self.base_url}/waInstance{self.instance_id}/{method}/{self.token}"

    async def _get_session(self) -> aiohttp.ClientSession:
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
#         sender = WhatsAppSender(settings)
#         await sender.send_text(chat_id="120363408049945016@g.us", text="whatsapp")
#         await sender.close()
#
#     asyncio.run(main())

