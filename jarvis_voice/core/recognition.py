import os
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
from jarvis_voice.utils.logger import logger

class RecognitionEngine:
    def __init__(self, sensitivity=0.5):
        self.q = queue.Queue()
        self.sensitivity = sensitivity
        self.model = None
        self.rec = None
        self.samplerate = 16000

        # Try to load Vosk model
        self.model_path = "model"
        if os.path.exists(self.model_path):
            try:
                self.model = Model(self.model_path)
                self.rec = KaldiRecognizer(self.model, self.samplerate)
                logger.info("Vosk модель успешно загружена.")
            except Exception as e:
                logger.error(f"Ошибка загрузки Vosk: {e}")

    def callback(self, indata, frames, time, status):
        if status:
            logger.error(status)
        self.q.put(bytes(indata))

    def listen(self):
        # If Vosk model is available, use it for offline recognition
        if self.model and self.rec:
            try:
                return self._listen_vosk()
            except Exception as e:
                logger.error(f"Ошибка Vosk: {e}")
                # Fallback to Google if Vosk fails

        # Fallback to SpeechRecognition (Google)
        return self._listen_google()

    def _listen_vosk(self):
        logger.info("Слушаю (Vosk оффлайн)...")
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, device=None,
                             dtype='int16', channels=1, callback=self.callback):
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "")
                    if text:
                        logger.info(f"Распознано (Vosk): {text}")
                        return text.lower()
                else:
                    # Partial result could be handled here if needed
                    pass

    def _listen_google(self):
        logger.info("Слушаю (Google онлайн)...")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language="ru-RU")
                logger.info(f"Распознано (Google): {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except Exception as e:
                logger.error(f"Ошибка распознавания Google: {e}")
                return None

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity
