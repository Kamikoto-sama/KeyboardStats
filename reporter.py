import datetime
import json
import os.path
import threading
from logging import Logger
from queue import Queue
from threading import Thread
from typing import override

class Reporter(Thread):
    save_delay = 60

    def __init__(self, base_path: str, log: Logger):
        super().__init__()
        self.log = log
        self.stopping = False
        self.base_path = base_path
        self.queue = Queue()
        self.chords_stat = dict()
        self.timer = threading.Timer(self.save_delay, self.save)
        self.stat_dt = datetime.date.today()

    def report(self, keys: list[str]):
        self.queue.put(keys)

    @override
    def run(self):
        self.try_load()
        self.timer.start()
        while not self.stopping:
            try:
                keys = self.queue.get()
                chord = "+".join([k.replace(" ", "_") for k in keys])
                if chord not in self.chords_stat:
                    self.chords_stat[chord] = 1
                else:
                    self.chords_stat[chord] += 1
            except Exception as e:
                self.log.error(e)

    def stop(self):
        self.stopping = True
        self.timer.cancel()

    def try_load(self):
        file = self.get_filename()
        if os.path.exists(file):
            with open(file) as f:
                data = f.read()
                self.chords_stat = json.loads(data)

    def save(self):
        self.reset_stats()
        self.chords_stat["$ts"] = f"{datetime.datetime.now().time()}"
        try:
            with open(self.get_filename(), "w") as f:
                data = json.dumps(self.chords_stat)
                f.write(data)
        except Exception as e:
            self.log.error(e)
        self.timer = threading.Timer(self.save_delay, self.save)
        self.timer.start()

    def reset_stats(self):
        today = datetime.date.today()
        if self.stat_dt == today:
            return
        self.chords_stat = dict()
        self.stat_dt = today

    def get_filename(self):
        return os.path.join(self.base_path, f"{datetime.date.today()}.json")
