import logging
import os
from logging.handlers import TimedRotatingFileHandler


def configure_logging():
    logger = logging.getLogger("my_logger")
    os.makedirs("logs", exist_ok=True)
    handler = TimedRotatingFileHandler(
        filename="logs/log",
        when="D",
        interval=1,
        backupCount=2,  # сколько старых файлов хранить
        encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    ))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
