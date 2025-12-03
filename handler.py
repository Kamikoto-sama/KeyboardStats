from logging import Logger

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

    def start(self):
        while not self.stopping:
            try:
                e = kb.read_event()
                self.handle(e)
            except Exception as e:
                self.log.error(e)

    def stop(self):
        self.stopping = True
