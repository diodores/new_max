from src.logging import log_state, logger


class MessageDispatcher:
    def __init__(self, sender):
        self.sender = sender

    async def handle(self, chat_id: str, data: dict):
        """
        Универсальная обработка сообщений:
        text / media / reaction / quoted
        """

        text = data.get("text")
        media_url = data.get("media_url")
        caption = data.get("caption")

        reaction = data.get("reaction")

        quoted_text = data.get("quoted_text")
        quoted_caption = data.get("quoted_caption")

        # 1. REACTION
        if reaction:
            try:
                await self.sender.send_text(
                    chat_id=chat_id,
                    text=f"❤️ {reaction}"
                )

                log_state("DISPATCH_REACTION", chat_id=chat_id)

            except Exception as e:
                logger.error("dispatch_reaction_failed chat_id=%s error=%s", chat_id, str(e))
                raise

            return

        # 2. MEDIA
        if media_url:
            try:
                await self.sender.send_file(
                    chat_id=chat_id,
                    file_url=media_url,
                    caption=caption
                )

                log_state("DISPATCH_FILE", chat_id=chat_id)

            except Exception as e:
                logger.error("dispatch_file_failed chat_id=%s error=%s", chat_id, str(e))
                raise

            return

        # 3. TEXT (+ QUOTED)
        if text:
            if quoted_text or quoted_caption:
                quoted_part = quoted_text or quoted_caption
                text = f"↩️ {quoted_part}\n\n➡️ {text}"

            try:
                await self.sender.send_text(
                    chat_id=chat_id,
                    text=text
                )

                log_state("DISPATCH_TEXT", chat_id=chat_id)

            except Exception as e:
                logger.error("dispatch_text_failed chat_id=%s error=%s", chat_id, str(e))
                raise

            return

        # 4. UNSUPPORTED
        try:
            await self.sender.send_text(
                chat_id=chat_id,
                text="[unsupported message type]"
            )

            log_state("DISPATCH_UNSUPPORTED", chat_id=chat_id)

        except Exception as e:
            logger.error("dispatch_unsupported_failed chat_id=%s error=%s", chat_id, str(e))
            raise