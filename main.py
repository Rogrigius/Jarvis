import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
# Это должно быть ПЕРВЫМ действием в скрипте
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import threading
import time
from PyQt6.QtWidgets import QApplication

# Выполняем импорты после настройки sys.path
from jarvis_voice.utils.config import ConfigManager
from jarvis_voice.utils.logger import logger
from jarvis_voice.core.speech import SpeechEngine
from jarvis_voice.core.recognition import RecognitionEngine
from jarvis_voice.core.plugin_manager import PluginManager
from jarvis_voice.core.command_engine import CommandEngine
from jarvis_voice.utils.activity_tracker import ActivityTracker
from jarvis_voice.gui.main_window import MainWindow

class Jarvis:
    def __init__(self):
        logger.info("Инициализация ДЖАРВИСА...")
        self.config = ConfigManager()
        self.speech = SpeechEngine()
        self.recognition = RecognitionEngine(
            sensitivity=self.config.get_setting("recognition_sensitivity", 0.5)
        )
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_plugins()
        self.command_engine = CommandEngine(self)
        self.activity_tracker = ActivityTracker(
            self, 
            limit_minutes=self.config.get_setting("user_activity_timer_minutes", 120)
        )
        
        self.running = False
        self.ui = None
        self.hotkey_thread = None

    def start(self):
        self.running = True
        self.activity_tracker.start()
        
        # Start voice recognition thread
        self.recognition_thread = threading.Thread(target=self._recognition_loop, daemon=True)
        self.recognition_thread.start()
        
        # Start Hotkey thread
        self.hotkey_thread = threading.Thread(target=self._setup_hotkeys, daemon=True)
        self.hotkey_thread.start()
        
        logger.info("Системы ДЖАРВИСА активны.")

    def stop(self):
        self.running = False
        self.activity_tracker.stop()
        logger.info("Выключение ДЖАРВИСА...")

    def _setup_hotkeys(self):
        try:
            from pynput import keyboard

            # Ctrl+Shift+J to wake up JARVIS
            hotkey = keyboard.HotKey(
                keyboard.HotKey.parse('<ctrl>+<shift>+j'),
                self._on_hotkey
            )

            with keyboard.Listener(
                    on_press=lambda k: hotkey.press(self.listener.canonical(k)),
                    on_release=lambda k: hotkey.release(self.listener.canonical(k))) as self.listener:
                self.listener.join()
        except Exception as e:
            logger.error(f"Ошибка настройки горячих клавиш: {e}")

    def _on_hotkey(self):
        logger.info("Горячая клавиша нажата!")
        if self.ui:
            self.ui.manual_trigger()
        self.speech.speak("Я слушаю вас, сэр.")

    def _recognition_loop(self):
        while self.running:
            try:
                text = self.recognition.listen()
                if text:
                    self.command_engine.process_text(text)
                    if self.ui:
                        self.ui.update_log(f"Пользователь: {text}")
            except Exception as e:
                logger.error(f"Ошибка в цикле распознавания: {e}")
            time.sleep(0.1)

    def ui_notify(self, title, message):
        if self.ui:
            self.ui.update_log(f"[{title}] {message}")

def main():
    app = QApplication(sys.argv)
    
    jarvis = Jarvis()
    window = MainWindow(jarvis)
    jarvis.ui = window
    
    jarvis.start()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
