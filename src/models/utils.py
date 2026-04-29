#my_project/maxbot_rebbit/src/models/utils.py
from datetime import datetime
from zoneinfo import ZoneInfo


def to_msk_datetime_str(ts: int) -> str:
    dt_utc = datetime.fromtimestamp(ts, tz=ZoneInfo("UTC"))
    dt_msk = dt_utc.astimezone(ZoneInfo("Europe/Moscow"))
    return dt_msk.strftime("%Y-%m-%d %H:%M:%S")


def extract_text(message_data: dict) -> str | None:
    if not message_data:
        return None

    text_block = message_data.get("textMessageData")
    if text_block:
        return text_block.get("textMessage")

    file_block = message_data.get("fileMessageData")
    if file_block:
        return file_block.get("caption")

    ext = message_data.get("extendedTextMessageData")
    if ext:
        return ext.get("text")

    return None


def extract_media(message_data: dict) -> str | None:
    if not message_data:
        return None

    file_block = message_data.get("fileMessageData")
    if file_block:
        return file_block.get("downloadUrl")

    return None

