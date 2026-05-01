def build_message(data: dict) -> dict | None:
    author = data.get("author", "unknown")
    text = data.get("text")
    media_url = data.get("media_url")
    caption = data.get("caption")
    reaction = data.get("reaction")

    quoted_text = data.get("quoted_text")
    quoted_caption = data.get("quoted_caption")
    reply_to = data.get("reply_to_message_id")

    time = data.get("datetime_msk", "")

    # -------------------------
    # EMOJI
    # -------------------------
    user_emoji = "👤"
    time_emoji = "🕒"
    reply_emoji = "↩️"
    msg_emoji = "💬"
    file_emoji = "📎"

    # -------------------------
    # 1. REACTION → IGNORE
    # -------------------------
    if reaction:
        return None

    # -------------------------
    # 2. FILE
    # -------------------------
    if media_url:
        return {
            "type": "file",
            "file_url": media_url,
            "caption": (
                f"{file_emoji} *Файл*\n"
                f"{user_emoji} {author}\n"
                f"{time_emoji} {time}\n\n"
                f"{caption or ''}"
            )
        }

    # -------------------------
    # 3. QUOTED (ВАЖНО: выше текста)
    # -------------------------
    if quoted_text or quoted_caption or reply_to:
        quoted = quoted_text or quoted_caption or "[сообщение недоступно]"

        return {
            "type": "text",
            "text": (
                f"{reply_emoji} *Ответ*\n"
                f"{user_emoji} *{author}*\n"
                f"{time_emoji} {time}\n\n"
                f"> {quoted}\n\n"
                f"{msg_emoji} {text or ''}"
            )
        }

    # -------------------------
    # 4. TEXT
    # -------------------------
    if text:
        return {
            "type": "text",
            "text": (
                f"{user_emoji} *{author}*\n"
                f"{time_emoji} {time}\n\n"
                f"{msg_emoji} {text}"
            )
        }

    return None