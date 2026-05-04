#/home/deb/my_project/maxbot_rebbit/src/senders/dispatcher.py
from src.logging_app import log_state, logger


class MessageDispatcher:
    def __init__(self, sender):
        self.sender = sender

    async def handle(self, chat_id: str, data: dict):

        text = data.get("text")
        media_url = data.get("media_url")
        caption = data.get("caption")

        reaction = data.get("reaction")

        quoted_text = data.get("quoted_text")
        quoted_caption = data.get("quoted_caption")

        # ---------------- REACTION ----------------
        if reaction:
            try:
                await self.sender.send_text(
                    chat_id=chat_id,
                    text=f"❤️ {reaction}"
                )
                log_state("DISPATCH_REACTION", chat_id=chat_id)

            except Exception as e:
                logger.error(
                    "dispatch_reaction_failed chat_id=%s error=%s",
                    chat_id,
                    str(e),
                    exc_info=True
                )
            return

        # ---------------- MEDIA ----------------
        if media_url:
            try:
                await self.sender.send_file(
                    chat_id=chat_id,
                    file_url=media_url,
                    caption=caption or ""
                )
                log_state("DISPATCH_FILE", chat_id=chat_id)

            except Exception as e:
                logger.error(
                    "dispatch_file_failed chat_id=%s error=%s",
                    chat_id,
                    str(e),
                    exc_info=True
                )
            return

        # ---------------- TEXT + QUOTE FIX ----------------
        if text:

            # 🔥 главный фикс: нормальный fallback цепочкой
            quoted_part = quoted_text or quoted_caption

            # 🔥 защита от пустых цитат типа "" или " "
            if quoted_part:
                quoted_part = quoted_part.strip()
                if not quoted_part:
                    quoted_part = None

            if quoted_part:
                text = (
                    f"↩️ {quoted_part}\n"
                    f"------\n"
                    f"➡️ {text}"
                )
            else:
                text = (
                    f"💬 {text}"
                )

            try:
                await self.sender.send_text(
                    chat_id=chat_id,
                    text=text
                )
                log_state("DISPATCH_TEXT", chat_id=chat_id)

            except Exception as e:
                logger.error(
                    "dispatch_text_failed chat_id=%s error=%s",
                    chat_id,
                    str(e),
                    exc_info=True
                )
            return

        # ---------------- FALLBACK ----------------
        try:
            await self.sender.send_text(
                chat_id=chat_id,
                text="[unsupported message type]"
            )
            log_state("DISPATCH_UNSUPPORTED", chat_id=chat_id)

        except Exception as e:
            logger.error(
                "dispatch_unsupported_failed chat_id=%s error=%s",
                chat_id,
                str(e),
                exc_info=True
            )

