import asyncio
import aiohttp

from src.senders.base import BaseSender
from src.config import Settings
from src.logging_app import log_state, logger


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
            log_state("HTTP_SESSION_CREATED", service="whatsapp")
        return self.session

    # TEXT
    async def send_text(self, chat_id: str, text: str) -> dict:
        session = await self._get_session()
        url = self._url("sendMessage")

        payload = {
            "chatId": chat_id,
            "message": text,
        }

        try:
            async with session.post(url, json=payload) as resp:
                data = await resp.json()

                if resp.status >= 400:
                    logger.error("wa_send_text_failed status=%s chat_id=%s response=%s", resp.status, chat_id, data)
                    raise Exception("WhatsApp API error")

                log_state("WA_TEXT_SENT", chat_id=chat_id)

                return data

        except Exception as e:
            logger.error("wa_send_text_exception chat_id=%s error=%s", chat_id, str(e), exc_info=True)
            raise

    # FILE
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

        try:
            async with session.post(url, json=payload) as resp:
                data = await resp.json()

                if resp.status >= 400:
                    logger.error(
                        "wa_send_file_failed status=%s chat_id=%s response=%s",
                        resp.status,
                        chat_id, data,
                        exc_info=True
                    )
                    raise Exception("WhatsApp API error")

                log_state("WA_FILE_SENT", chat_id=chat_id)

                return data

        except Exception as e:
            logger.error("wa_send_file_exception chat_id=%s error=%s", chat_id, str(e), exc_info=True)
            raise

    # CLOSE
    async def close(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None
            log_state("HTTP_SESSION_CLOSED", service="whatsapp")


if __name__ == "__main__":
    async def main():
        settings = Settings()
        sender = WhatsAppSender(settings)
        await sender.send_text(
            chat_id="120363408049945016@g.us",
            text="whatsapp"
        )
        await sender.close()

    asyncio.run(main())
