#/home/deb/my_project/maxbot_rebbit/src/senders/utils.py
from src.logging_app import log_state, logger


def build_message(data: dict) -> dict | None:
    logger.info(f"build_message: {data}")
    author = data.get("author", "unknown")
    text = data.get("text")
    media_url = data.get("media_url")
    caption = data.get("caption")
    reaction = data.get("reaction")

    quoted_text = data.get("quoted_text")
    quoted_caption = data.get("quoted_caption")
    reply_to = data.get("reply_to_message_id")

    is_forwarded = data.get("is_forwarded", False)

    time = data.get("datetime_msk", "")

    # EMOJI
    user_emoji = "👤"
    time_emoji = "🕒"
    reply_emoji = "↩️"
    forward_emoji = "📤"
    msg_emoji = "💬"
    file_emoji = "📎"

    # REACTION
    if reaction:
        log_state("MESSAGE_SKIPPED", reason="reaction")
        return None

    # FILE
    if media_url:
        return {
            "type": "file",
            "file_url": media_url,
            "caption": (
                f"{file_emoji} Файл\n"
                f"{user_emoji} {author}\n"
                f"{time_emoji} {time}\n\n"
                f"{caption or ''}"
            )
        }

    # FORWARDED
    if is_forwarded:
        return {
            "type": "text",
            "text": (
                f"{forward_emoji} Пересланное сообщение\n"
                f"{user_emoji} {author}\n"
                f"{time_emoji} {time}\n\n"
                f"{msg_emoji} {text or ''}"
            )
        }

    # REPLY (FIXED FALLBACK)
    if quoted_text or quoted_caption or reply_to:
        quoted = quoted_text or quoted_caption or text or "[сообщение недоступно]"

        return {
            "type": "text",
            "text": (
                f"{user_emoji} {author}\n"
                f"{reply_emoji} Ответ на:\n"
                f"------\n"
                f"{quoted}\n"
                f"------\n"
                f"{msg_emoji} {text or ''}\n"
                f"{time_emoji} {time}"
            )
        }

    # TEXT
    if text:
        return {
            "type": "text",
            "text": (
                f"{user_emoji} {author}\n"
                f"{msg_emoji} {text}\n\n"
                f"{time_emoji} {time}"
            )
        }

    log_state("MESSAGE_DROPPED", reason="unknown_format")
    return None

