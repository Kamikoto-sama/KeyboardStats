import logging
import os
from logging.handlers import TimedRotatingFileHandler


def configure_logging():
    logger = logging.getLogger()
    os.makedirs("logs", exist_ok=True)
    handler = TimedRotatingFileHandler(
        filename="logs/log",
        when="D",
        interval=1,
        backupCount=2,  # сколько старых файлов хранить
        encoding="utf-8",
        utc=False
    )
    logger.addHandler(handler)
    return logger
