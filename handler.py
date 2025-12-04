from logging import Logger
import threading

import keyboard as kb

from layout import SystemLayout
from reporter import Reporter

modifiers = [m for m in kb.all_modifiers if "left" not in m and "right" not in m]

class Handler:
    stopping = False

    def __init__(self, reporter: Reporter, log: Logger):
        self.log = log
        self.reporter = reporter


    def handle(self, event: kb.KeyboardEvent):
        event_name = event.name
        if kb.is_modifier(event_name) or event.event_type == "up":
            return

        keys = [mod for mod in modifiers if kb.is_pressed(mod)]
        has_mods = len(keys) > 0
        keys.append(event_name)
        layout = SystemLayout.get_layout()
        if layout != "EN" and not has_mods:
            keys.append(f"|{layout}")
        self.reporter.report(keys)
        self.set_release_win()

    def start(self):
        while not self.stopping:
            try:
                e = kb.read_event()
                self.handle(e)
            except Exception as e:
                self.log.error(e)

    def stop(self):
        self.stopping = True

    def set_release_win(self):
        if kb.is_pressed("windows"):
            self.log.info("Win release set")
            threading.Timer(2, self.release_win).start()

    def release_win(self):
        try:
            kb.release('windows')
            kb.release('left windows')
            kb.release('right windows')
            kb._pressed_events.pop(91, None)
            self.log.info("Win released")
        except Exception as e:
            self.log.error(e)