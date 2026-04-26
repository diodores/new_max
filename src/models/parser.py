from datetime import datetime, timezone, timedelta
from src.models.raw import RawWebhook
from src.models.normalized import NormalizedMessage
from src.models.chat_map import CHAT_MAP


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
    media_url = None
    file_name = None
    caption = None

    # -------- TEXT --------
    if msg["typeMessage"] == "textMessage":
        text = msg["textMessageData"]["textMessage"]

    # -------- MEDIA --------
    file_data = msg.get("fileMessageData")

    if file_data:
        media_url = file_data.get("downloadUrl")
        caption = file_data.get("caption") or ""
        file_name = file_data.get("fileName")

        if msg["typeMessage"] == "documentMessage":
            if not caption:
                caption = file_name

    # -------- REPLY --------
    quoted = msg.get("quotedMessage")

    reply_to_message_id = None

    if quoted:
        reply_to_message_id = quoted.get("stanzaId")

    # -------- TIME --------
    dt_msk = datetime.fromtimestamp(timestamp, MSK).strftime("%Y-%m-%d %H:%M:%S")

    # -------- ROUTING --------
    routing_key = f"{CHAT_MAP.get(chat_id)}"
    #routing_key = f"{platform}.{chat_id}"

    return NormalizedMessage(
        platform=platform,
        chat_id=chat_id,
        chat_name=chat_name,
        author=author,

        text=text,
        media_url=media_url,
        file_name=file_name,
        caption=caption,

        reply_to_message_id=reply_to_message_id,

        event=event,
        timestamp=timestamp,
        datetime_msk=dt_msk,

        message_id=raw.idMessage,
        routing_key=routing_key,
    )