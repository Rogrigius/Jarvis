from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QPushButton, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QTimer
from jarvis_voice.gui.styles import STYLE_SHEET
from jarvis_voice.gui.command_editor import CommandEditor
from jarvis_voice.gui.settings_window import SettingsWindow
from jarvis_voice.utils.logger import logger

class MainWindow(QMainWindow):
    def __init__(self, jarvis_context):
        super().__init__()
        self.jarvis = jarvis_context
        self.setWindowTitle("ДЖАРВИС - Футуристичный голосовой помощник")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(STYLE_SHEET)
        
        self.init_ui()
        self.init_tray()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        self.status_label = QLabel("СТАТУС: ОЖИДАНИЕ")
        self.status_label.setStyleSheet("font-size: 18px; color: #00d4ff; font-weight: bold;")
        header_layout.addWidget(self.status_label)
        
        self.voice_viz = QLabel("● ● ● ● ●")
        self.voice_viz.setStyleSheet("font-size: 24px; color: #16213e;")
        header_layout.addStretch()
        header_layout.addWidget(self.voice_viz)
        
        main_layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Dashboard
        self.dashboard = QWidget()
        dash_layout = QVBoxLayout(self.dashboard)
        self.log_display = QLabel("Инициализация систем...\nВсе системы в норме.\nГотов к работе, сэр.")
        self.log_display.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.log_display.setStyleSheet("background-color: #0b0f19; border: 1px solid #00d4ff; padding: 10px; font-family: 'Consolas', monospace;")
        dash_layout.addWidget(self.log_display)
        
        self.listen_btn = QPushButton("РУЧНОЙ ЗАПУСК")
        self.listen_btn.clicked.connect(self.manual_trigger)
        dash_layout.addWidget(self.listen_btn)
        
        self.tabs.addTab(self.dashboard, "ПАНЕЛЬ")
        
        # Command Editor
        self.command_editor = CommandEditor(self.jarvis)
        self.tabs.addTab(self.command_editor, "КОМАНДЫ")
        
        # Settings
        self.settings_window = SettingsWindow(self.jarvis)
        self.tabs.addTab(self.settings_window, "НАСТРОЙКИ")
        
        main_layout.addWidget(self.tabs)
        
        # Footer
        footer = QLabel("ДЖАРВИС v1.0.0 | Пользователь: " + self.jarvis.config.get("user_profile", {}).get("name", "Сэр"))
        footer.setStyleSheet("font-size: 10px; color: #555;")
        main_layout.addWidget(footer)

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Показать")
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Выход")
        quit_action.triggered.connect(self.close_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def manual_trigger(self):
        logger.info("Ручной запуск активирован")
        self.status_label.setText("СТАТУС: СЛУШАЮ")
        self.voice_viz.setStyleSheet("font-size: 24px; color: #00d4ff;")
        QTimer.singleShot(2000, self.reset_status)

    def reset_status(self):
        self.status_label.setText("СТАТУС: ОЖИДАНИЕ")
        self.voice_viz.setStyleSheet("font-size: 24px; color: #16213e;")

    def update_log(self, text):
        current_text = self.log_display.text()
        lines = current_text.split("\n")
        lines.append(text)
        if len(lines) > 20:
            lines = lines[-20:]
        self.log_display.setText("\n".join(lines))

    def close_app(self):
        self.jarvis.stop()
        self.close()

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.close_app()
            event.accept()
