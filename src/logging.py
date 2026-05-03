import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    # убрать дубли
    logger.handlers.clear()


    # 1. BUSINESS FORMAT (INFO)

    business_handler = logging.StreamHandler(sys.stdout)
    business_handler.setLevel(logging.INFO)

    business_formatter = logging.Formatter(
        "%(asctime)s | INFO | %(message)s"
    )
    business_handler.setFormatter(business_formatter)


    # 2. SYSTEM FORMAT (WARNING+ERROR)
    system_handler = logging.StreamHandler(sys.stdout)
    system_handler.setLevel(logging.WARNING)

    system_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )
    system_handler.setFormatter(system_formatter)


    # FILE (ERROR ONLY)
    file_handler = RotatingFileHandler(
        "/app/logs/app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=2
    )
    file_handler.setLevel(logging.ERROR)

    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # handlers
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
    """ Логирование бизнес-состояний системы. Используется вместо множества print/info/debug. """
    msg = f"[STATE={state}]"
    if context:
        msg += " " + " ".join(f"{k}={v}" for k, v in context.items())

    logger.info(msg)