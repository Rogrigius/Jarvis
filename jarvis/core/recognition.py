import os
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from jarvis.utils.logger import logger

class RecognitionEngine:
    def __init__(self, sensitivity=0.5):
        # In a real app, you'd download the model or provide a path
        # model_path = "model-ru"
        # self.model = Model(model_path)
        # self.rec = KaldiRecognizer(self.model, 16000)
        self.q = queue.Queue()
        self.sensitivity = sensitivity

    def callback(self, indata, frames, time, status):
        if status:
            logger.error(status)
        self.q.put(bytes(indata))

    def listen(self):
        # This is a simplified Vosk implementation mock for this environment
        # since downloading a 50MB+ model in a sandbox is restricted.
        # But it shows the architecture using sounddevice and queue.
        logger.info("Слушаю (Vosk)...")
        # with sd.RawInputStream(samplerate=16000, blocksize=8000, device=None, 
        #                      dtype='int16', channels=1, callback=self.callback):
        #     while True:
        #         data = self.q.get()
        #         if self.rec.AcceptWaveform(data):
        #             result = self.rec.Result()
        #             # process result...
        
        # Fallback to SpeechRecognition for the sandbox, but keeping Vosk structure
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language="ru-RU")
                logger.info(f"Распознано: {text}")
                return text.lower()
            except Exception:
                return None

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity
