import os
import signal

from handler import Handler
from logger import configure_logging
from reporter import Reporter


def stop(*args):
    exit(0)


log = configure_logging()
os.makedirs("reports", exist_ok=True)
reporter = Reporter("reports", log)
handler = Handler(reporter)
signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
reporter.start()
handler.start()
