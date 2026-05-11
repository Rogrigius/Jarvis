import time
import threading
from jarvis.utils.logger import logger

class ActivityTracker:
    def __init__(self, jarvis_context, limit_minutes=120):
        self.jarvis = jarvis_context
        self.limit_seconds = limit_minutes * 60
        self.start_time = time.time()
        self.running = False
        self._thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self._thread = threading.Thread(target=self._monitor, daemon=True)
            self._thread.start()
            logger.info("Трекер активности запущен.")

    def stop(self):
        self.running = False
        logger.info("Трекер активности остановлен.")

    def _monitor(self):
        while self.running:
            elapsed = time.time() - self.start_time
            if elapsed >= self.limit_seconds:
                self._trigger_notification(elapsed)
                self.start_time = time.time()
            
            time.sleep(60)

    def _trigger_notification(self, elapsed):
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        
        message = ""
        if hours > 0:
            message = f"Вы работаете уже {hours} час(а) и {minutes} минут(ы). Рекомендую сделать небольшой перерыв."
        else:
            message = f"Вы работаете уже {minutes} минут(ы). Рекомендую сделать небольшой перерыв."
        
        logger.info(f"Уведомление об активности: {message}")
        self.jarvis.speech.speak(message)
        
        suggestions = [
            "Пора размяться, сэр.",
            "Не забудьте выпить немного воды.",
            "Дайте вашим глазам отдохнуть, сэр."
        ]
        import random
        self.jarvis.speech.speak(random.choice(suggestions))
        
        if hasattr(self.jarvis, 'ui_notify'):
            self.jarvis.ui_notify("Напоминание о перерыве", message)

    def update_limit(self, minutes):
        self.limit_seconds = minutes * 60
        logger.info(f"Лимит трекера активности обновлен до {minutes} минут.")
