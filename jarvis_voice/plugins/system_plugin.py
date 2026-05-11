import os
from datetime import datetime
from jarvis_voice.plugins.plugin_base import PluginBase
from jarvis_voice.utils.logger import logger

class SystemPlugin(PluginBase):
    def get_commands(self):
        return {
            "который час": "get_time",
            "какое сегодня число": "get_date",
            "выключи систему": "system_shutdown"
        }

    def get_time(self):
        now = datetime.now().strftime("%H:%M")
        self.jarvis.speech.speak(f"Сейчас {now}, сэр.")
        return True

    def get_date(self):
        today = datetime.now().strftime("%A, %d %B")
        self.jarvis.speech.speak(f"Сегодня {today}.")
        return True

    def system_shutdown(self):
        self.jarvis.speech.speak("Последовательность завершения системы инициирована. Шучу, я не буду этого делать без надлежащей авторизации.")
        return True
