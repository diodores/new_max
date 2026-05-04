#/home/deb/my_project/maxbot_rebbit/src/logging_app.py
import logging
import os
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    # важно: чтобы не плодились хендлеры при повторных импортax
    logger.handlers.clear()

    # 📌 фиксируем корень проекта (src -> project root)
    BASE_DIR = Path(__file__).resolve().parents[1]

    # 📌 единая директория логов
    log_dir = Path(os.getenv("LOG_DIR", BASE_DIR / "logs"))
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "app.log"

    # ---------------- BUSINESS LOGS (INFO) ----------------
    business_handler = logging.StreamHandler(sys.stdout)
    business_handler.setLevel(logging.INFO)
    business_handler.setFormatter(logging.Formatter(
        "%(asctime)s | INFO | %(message)s"
    ))

    # ---------------- SYSTEM LOGS (WARNING+) ----------------
    system_handler = logging.StreamHandler(sys.stdout)
    system_handler.setLevel(logging.WARNING)
    system_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d | %(message)s"
    ))

    # ---------------- FILE LOGS (ERROR ONLY) ----------------
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=2
    )
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d | %(message)s"
    ))

    # ---------------- ATTACH ----------------
    logger.addHandler(business_handler)
    logger.addHandler(system_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()


def log_block_start(title: str):
    logger.info("")
    logger.info("=" * 90)
    logger.info(f"▶ START: MESSAGE {title}")
    logger.info("=" * 90)


def log_block_end(title: str):
    logger.info("=" * 90)
    logger.info(f"■ END: MESSAGE SENT TO: {title}")
    logger.info("=" * 90)
    logger.info("")


def log_state(state: str, **context):
    """Логирование бизнес-состояний системы."""
    msg = f"[STATE={state}]"
    if context:
        msg += " " + " ".join(f"{k}={v}" for k, v in context.items())

    logger.info(msg)