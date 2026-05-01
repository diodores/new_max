#my_project/maxbot_rebbit/src/models/parser.py

from datetime import datetime, timezone, timedelta
from src.models.raw import RawWebhook
from src.models.normalized import NormalizedMessage


MSK = timezone(timedelta(hours=3))


def parse_webhook(raw: RawWebhook, platform: str) -> NormalizedMessage:
    sender = raw.senderData
    msg = raw.messageData

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
    quoted_media_url = None
    quoted_file_name = None
    quoted_caption = None

    msg_type = msg.get("typeMessage")

    # -------- TEXT --------
    if msg_type == "textMessage":
        text = msg.get("textMessageData", {}).get("textMessage")

    elif msg_type == "quotedMessage":
        text = msg.get("extendedTextMessageData", {}).get("text")

    elif msg_type == "reactionMessage":
        reaction = msg.get("extendedTextMessageData", {}).get("text")

    # -------- MEDIA --------
    file_data = msg.get("fileMessageData")

    if file_data:
        media_url = file_data.get("downloadUrl")
        caption = file_data.get("caption") or ""
        file_name = file_data.get("fileName")

        if msg_type == "documentMessage" and not caption:
            caption = file_name

    # -------- QUOTED (универсально) --------
    quoted_block = msg.get("quotedMessage")

    if quoted_block:
        q_type = quoted_block.get("typeMessage")

        if q_type == "textMessage":
            quoted_text = (
                quoted_block.get("textMessageData", {})
                            .get("textMessage")
            )

        elif q_type in ["imageMessage", "videoMessage", "documentMessage"]:
            quoted_caption = quoted_block.get("caption")
            quoted_file_name = quoted_block.get("fileName")
            quoted_media_url = quoted_block.get("downloadUrl")

            if not quoted_caption:
                quoted_caption = f"[{q_type}]"

    # -------- REPLY META --------
    reply_to_message_id = (
        quoted_block.get("stanzaId") if quoted_block else None
    )

    # -------- TIME --------
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
        quoted_media_url=quoted_media_url,
        quoted_file_name=quoted_file_name,
        quoted_caption=quoted_caption,

        reply_to_message_id=reply_to_message_id,

        event=event,
        timestamp=timestamp,
        datetime_msk=dt_msk,

        message_id=raw.idMessage,
    )