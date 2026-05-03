import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)


    # CONSOLE

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    console_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    )
    console_handler.setFormatter(console_formatter)


    # FILE
    file_handler = RotatingFileHandler(
        "/app/logs/app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=2
    )
    file_handler.setLevel(logging.ERROR)

    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # cleanup (важно чтобы не было дублей при reload)
    logger.handlers.clear()

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()

def log_state(state: str, **context):
    """
    Логирование бизнес-состояний системы.
    Используется вместо множества print/info/debug.
    """
    msg = f"[STATE={state}]"

    if context:
        msg += " " + " ".join(f"{k}={v}" for k, v in context.items())

    logger.info(msg)