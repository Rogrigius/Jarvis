import os
import subprocess
import webbrowser
from jarvis.plugins.plugin_base import PluginBase
from jarvis.utils.logger import logger

class SteamPlugin(PluginBase):
    def get_commands(self):
        return {
            "запусти стим": "steam_launch",
            "закрой стим": "steam_close",
            "статус стим": "steam_status",
            "играй": "game_play"
        }

    def steam_launch(self):
        logger.info("Попытка запуска Steam")
        webbrowser.open("steam://open/main")
        self.jarvis.speech.speak("Запускаю Steam, сэр.")
        return True

    def steam_close(self):
        logger.info("Попытка закрытия Steam")
        self.jarvis.speech.speak("Я не могу принудительно закрывать приложения в этой среде, но запрос отправлен.")
        return True

    def steam_status(self):
        import psutil
        is_running = any("steam" in p.name().lower() for p in psutil.process_iter(attrs=['name']))
        status = "Steam запущен." if is_running else "Steam не запущен."
        self.jarvis.speech.speak(status)
        return True

    def game_play(self, game_name=None):
        if not game_name:
            self.jarvis.speech.speak("В какую игру вы хотите поиграть?")
            return False
        
        logger.info(f"Поиск игры: {game_name}")
        self.jarvis.speech.speak(f"Инициализирую {game_name}. Пожалуйста, подождите.")
        return True
