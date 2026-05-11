import pyttsx3
import threading
import os
from jarvis_voice.utils.logger import logger

class SpeechEngine:
    def __init__(self, rate=175, volume=1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "russian" in voice.name.lower() or "ru" in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self._lock = threading.Lock()

    def speak(self, text_or_path):
        if not text_or_path:
            return

        # Check if text_or_path is a path to an existing audio file
        if os.path.exists(text_or_path) and text_or_path.lower().endswith(('.wav', '.mp3')):
            self.play_audio(text_or_path)
        else:
            self.say_text(text_or_path)

    def say_text(self, text):
        def _speak():
            with self._lock:
                logger.info(f"Произношу: {text}")
                self.engine.say(text)
                self.engine.runAndWait()

        threading.Thread(target=_speak).start()

    def play_audio(self, file_path):
        def _play():
            with self._lock:
                logger.info(f"Воспроизвожу файл: {file_path}")
                # Simple audio playback implementation
                # On Windows: os.startfile(file_path) or use a library
                # For this implementation, we use a generic placeholder
                try:
                    import playsound
                    playsound.playsound(file_path)
                except ImportError:
                    pass

        threading.Thread(target=_play).start()

    def set_rate(self, rate):
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        self.engine.setProperty('volume', volume)
