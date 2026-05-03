import aiohttp
import asyncio

from src.senders.base import BaseSender
from src.config import Settings
from src.logging import log_state, logger


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
            log_state("HTTP_SESSION_CREATED", service="max")
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
                    logger.error( "max_send_text_failed status=%s chat_id=%s response=%s", resp.status, chat_id, data)
                    raise Exception("Max API error")

                log_state("MAX_TEXT_SENT", chat_id=chat_id)

                return data

        except Exception as e:
            logger.error("max_send_text_exception chat_id=%s error=%s", chat_id, str(e))
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
                    logger.error("max_send_file_failed status=%s chat_id=%s response=%s", resp.status, chat_id, data)
                    raise Exception("Max API error")

                log_state("MAX_FILE_SENT", chat_id=chat_id)

                return data

        except Exception as e:
            logger.error("max_send_file_exception chat_id=%s error=%s", chat_id, str(e))
            raise

    # CLOSE
    async def close(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None
            log_state("HTTP_SESSION_CLOSED", service="max")