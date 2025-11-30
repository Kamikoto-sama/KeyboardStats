import ctypes

user32 = ctypes.WinDLL("user32", use_last_error=True)
# Таблица для RU/EN
lang_map = {
    0x419: "RU",
    0x409: "EN",
    0x411: "JP"
}


class SystemLayout:


    @staticmethod
    def get_layout():
        # Получаем текущий thread id и layout
        thread_id = user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), 0)
        layout_id = user32.GetKeyboardLayout(thread_id)

        # layout_id содержит язык в младших 16 битах
        lang_id = layout_id & 0xFFFF

        return lang_map.get(lang_id, hex(lang_id))
