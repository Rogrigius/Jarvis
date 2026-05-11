from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QSlider, QComboBox, QCheckBox, QSpinBox, QLabel, QPushButton
from PyQt6.QtCore import Qt
from jarvis.utils.logger import logger
from jarvis.utils.startup import add_to_startup, remove_from_startup

class SettingsWindow(QWidget):
    def __init__(self, jarvis_context):
        super().__init__()
        self.jarvis = jarvis_context
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Настройки ДЖАРВИСА")
        layout.addWidget(self.label)
        
        form_layout = QFormLayout()
        
        self.sensitivity_slider = QSlider(Qt.Orientation.Horizontal)
        self.sensitivity_slider.setRange(0, 100)
        current_sens = self.jarvis.config.get_setting("recognition_sensitivity", 0.5)
        self.sensitivity_slider.setValue(int(current_sens * 100))
        form_layout.addRow("Чувствительность голоса:", self.sensitivity_slider)
        
        self.mic_combo = QComboBox()
        self.mic_combo.addItems(["Микрофон по умолчанию", "Встроенный микрофон", "USB-аудиоустройство"])
        form_layout.addRow("Источник микрофона:", self.mic_combo)
        
        self.timer_spin = QSpinBox()
        self.timer_spin.setRange(1, 480)
        self.timer_spin.setSuffix(" минут")
        current_timer = self.jarvis.config.get_setting("user_activity_timer_minutes", 120)
        self.timer_spin.setValue(current_timer)
        form_layout.addRow("Напоминание об активности:", self.timer_spin)
        
        self.notif_check = QCheckBox("Включить уведомления в интерфейсе")
        self.notif_check.setChecked(self.jarvis.config.get_setting("notifications_enabled", True))
        form_layout.addRow(self.notif_check)
        
        self.startup_check = QCheckBox("Запускать при старте Windows")
        self.startup_check.setChecked(self.jarvis.config.get_setting("startup_enabled", False))
        form_layout.addRow(self.startup_check)
        
        layout.addLayout(form_layout)
        
        self.save_btn = QPushButton("Применить настройки")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)
        
        self.setLayout(layout)

    def save_settings(self):
        sens = self.sensitivity_slider.value() / 100.0
        timer = self.timer_spin.value()
        notif = self.notif_check.isChecked()
        startup = self.startup_check.isChecked()
        
        self.jarvis.config.set_setting("recognition_sensitivity", sens)
        self.jarvis.config.set_setting("user_activity_timer_minutes", timer)
        self.jarvis.config.set_setting("notifications_enabled", notif)
        self.jarvis.config.set_setting("startup_enabled", startup)
        
        if startup:
            add_to_startup()
        else:
            remove_from_startup()
        
        self.jarvis.recognition.set_sensitivity(sens)
        self.jarvis.activity_tracker.update_limit(timer)
        
        logger.info("Настройки обновлены через GUI.")
