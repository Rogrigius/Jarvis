import json
import os

DEFAULT_CONFIG = {
    "name": "ДЖАРВИС",
    "version": "1.0.0",
    "settings": {
        "recognition_sensitivity": 0.5,
        "microphone_index": None,
        "notifications_enabled": True,
        "user_activity_timer_minutes": 120,
        "theme": "dark",
        "startup_enabled": False
    },
    "user_profile": {
        "name": "Сэр",
        "work_duration_limit": 120
    },
    "commands": [
        {"phrase": "привет", "action": "greet", "response": "Здравствуйте, сэр. Чем могу помочь?"},
        {"phrase": "сколько времени", "action": "get_time", "response": "Сейчас {time}"},
        {"phrase": "открой стим", "action": "steam_launch", "response": "Открываю Steam для вас."},
        {"phrase": "включи музыку", "action": "music_play", "response": "Запускаю ваш плейлист в Яндекс Музыке."}
    ]
}

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG

    def save_config(self, config=None):
        if config:
            self.config = config
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def get_setting(self, setting_name, default=None):
        return self.config.get("settings", {}).get(setting_name, default)

    def set_setting(self, setting_name, value):
        if "settings" not in self.config:
            self.config["settings"] = {}
        self.config["settings"][setting_name] = value
        self.save_config()
