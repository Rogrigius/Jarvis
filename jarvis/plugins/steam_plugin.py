import os
import psutil
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
        # On Windows, steam:// protocol works well
        webbrowser.open("steam://open/main")
        self.jarvis.speech.speak("Запускаю Steam, сэр.")
        return True

    def steam_close(self):
        logger.info("Попытка закрытия Steam")
        closed = False
        for proc in psutil.process_iter(['name']):
            try:
                if "steam" in proc.info['name'].lower():
                    proc.terminate()
                    closed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if closed:
            self.jarvis.speech.speak("Steam был закрыт.")
        else:
            self.jarvis.speech.speak("Steam не запущен или мне не удалось его закрыть.")
        return True

    def steam_status(self):
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
