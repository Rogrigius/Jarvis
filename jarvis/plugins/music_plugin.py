import webbrowser
from jarvis.plugins.plugin_base import PluginBase
from jarvis.utils.logger import logger

class MusicPlugin(PluginBase):
    def get_commands(self):
        return {
            "музыка": "music_control",
            "включи музыку": "music_play",
            "пауза": "music_pause",
            "следующий трек": "music_next",
            "предыдущий трек": "music_prev",
            "громче": "volume_up",
            "тише": "volume_down"
        }

    def music_play(self):
        logger.info("Запуск Яндекс Музыки")
        webbrowser.open("https://music.yandex.ru/home")
        self.jarvis.speech.speak("Запускаю воспроизведение в Яндекс Музыке.")
        return True

    def music_pause(self):
        try:
            from pynput.keyboard import Key, Controller
            keyboard = Controller()
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
            self.jarvis.speech.speak("Музыка на паузе.")
        except Exception:
            self.jarvis.speech.speak("Я не смог управлять воспроизведением.")
        return True

    def music_next(self):
        try:
            from pynput.keyboard import Key, Controller
            keyboard = Controller()
            keyboard.press(Key.media_next)
            keyboard.release(Key.media_next)
            self.jarvis.speech.speak("Следующий трек.")
        except Exception:
            pass
        return True

    def music_prev(self):
        try:
            from pynput.keyboard import Key, Controller
            keyboard = Controller()
            keyboard.press(Key.media_previous)
            keyboard.release(Key.media_previous)
            self.jarvis.speech.speak("Предыдущий трек.")
        except Exception:
            pass
        return True

    def volume_up(self):
        try:
            from pynput.keyboard import Key, Controller
            keyboard = Controller()
            for _ in range(5):
                keyboard.press(Key.media_volume_up)
                keyboard.release(Key.media_volume_up)
            self.jarvis.speech.speak("Громкость увеличена.")
        except Exception:
            pass
        return True

    def volume_down(self):
        try:
            from pynput.keyboard import Key, Controller
            keyboard = Controller()
            for _ in range(5):
                keyboard.press(Key.media_volume_down)
                keyboard.release(Key.media_volume_down)
            self.jarvis.speech.speak("Громкость уменьшена.")
        except Exception:
            pass
        return True
    
    def music_control(self, action):
        if "играй" in action or "включи" in action: return self.music_play()
        if "пауза" in action: return self.music_pause()
        if "дальше" in action: return self.music_next()
        return False
