#/home/deb/my_project/maxbot_rebbit/src/models/parser.py
from datetime import datetime, timezone, timedelta

from src.models.raw import RawWebhook
from src.models.normalized import NormalizedMessage

MSK = timezone(timedelta(hours=3))


def parse_webhook(raw: RawWebhook, platform: str) -> NormalizedMessage:
    sender = raw.senderData
    msg = raw.messageData or {}

    chat_id = sender.get("chatId")
    chat_name = sender.get("chatName")
    author = sender.get("senderName")

    event = raw.typeWebhook
    timestamp = raw.timestamp

    text = None
    reaction = None

    media_url = None
    file_name = None
    caption = None

    quoted_text = None

    msg_type = msg.get("typeMessage")
    ext = msg.get("extendedTextMessageData", {})

    # ---------------- TEXT ----------------
    if msg_type == "textMessage":
        text = msg.get("textMessageData", {}).get("textMessage")

    elif msg_type == "extendedTextMessage":
        text = ext.get("text")

    elif msg_type == "reactionMessage":
        reaction = ext.get("text")

    # ---------------- MEDIA ----------------
    file_data = msg.get("fileMessageData")
    if file_data:
        media_url = file_data.get("downloadUrl")
        caption = file_data.get("caption") or ""
        file_name = file_data.get("fileName")

    # ---------------- QUOTE FIX (ВАЖНО) ----------------

    quoted_block = msg.get("quotedMessage")

    if quoted_block:
        quoted_text = (
            quoted_block.get("textMessage")
            or quoted_block.get("textMessageData", {}).get("textMessage")
        )

    # 🔥 ГЛАВНЫЙ FIX: WhatsApp reply text ВСЕГДА здесь
    if msg_type == "quotedMessage":
        text = ext.get("text")

        # если есть quotedMessage, берём его как fallback
        if not quoted_text:
            quoted_text = text

    # ---------------- REPLY META ----------------
    reply_to_message_id = (
        quoted_block.get("stanzaId") if quoted_block else None
    )

    # ---------------- FORWARDED ----------------
    is_forwarded = False

    if msg_type == "extendedTextMessage":
        is_forwarded = ext.get("isForwarded", False)

    # ---------------- TIME ----------------
    dt_msk = datetime.fromtimestamp(timestamp, MSK).strftime("%Y-%m-%d %H:%M:%S")

    return NormalizedMessage(
        platform=platform,
        chat_id=chat_id,
        chat_name=chat_name,
        author=author,

        text=text,
        reaction=reaction,

        media_url=media_url,
        file_name=file_name,
        caption=caption,

        quoted_text=quoted_text,

        is_forwarded=is_forwarded,

        reply_to_message_id=reply_to_message_id,

        event=event,
        timestamp=timestamp,
        datetime_msk=dt_msk,

        message_id=raw.idMessage,
    )

