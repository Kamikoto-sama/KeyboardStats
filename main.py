import os
import signal

from handler import Handler
from logger import configure_logging
from reporter import Reporter


def stop(*args):
    exit(0)


logger = configure_logging()
os.makedirs("reports", exist_ok=True)
reporter = Reporter("reports", logger)
handler = Handler(reporter, logger)
signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
reporter.start()
handler.start()
