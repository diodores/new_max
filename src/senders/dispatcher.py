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

        # -------------------------
        # 1. REACTION
        # -------------------------
        if reaction:
            await self.sender.send_text(
                chat_id=chat_id,
                text=f"❤️ {reaction}"
            )
            return

        # -------------------------
        # 2. MEDIA
        # -------------------------
        if media_url:
            await self.sender.send_file(
                chat_id=chat_id,
                file_url=media_url,
                caption=caption
            )
            return

        # -------------------------
        # 3. TEXT + QUOTED MESSAGE
        # -------------------------
        if text:
            if quoted_text or quoted_caption:
                quoted_part = quoted_text or quoted_caption
                text = f"↩️ {quoted_part}\n\n➡️ {text}"

            await self.sender.send_text(
                chat_id=chat_id,
                text=text
            )
            return

        # -------------------------
        # 4. EMPTY / UNSUPPORTED
        # -------------------------
        await self.sender.send_text(
            chat_id=chat_id,
            text="[unsupported message type]"
        )