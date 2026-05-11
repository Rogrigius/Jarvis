from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QLineEdit, QPushButton, QFormLayout
from jarvis.utils.logger import logger

class CommandEditor(QWidget):
    def __init__(self, jarvis_context):
        super().__init__()
        self.jarvis = jarvis_context
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Конфигурация команд")
        layout.addWidget(self.label)
        
        self.command_list = QListWidget()
        self.refresh_list()
        self.command_list.itemClicked.connect(self.load_command)
        layout.addWidget(self.command_list)
        
        form_layout = QFormLayout()
        self.phrase_input = QLineEdit()
        self.action_input = QLineEdit()
        self.response_input = QLineEdit()
        
        form_layout.addRow("Голосовая фраза:", self.phrase_input)
        form_layout.addRow("Действие/Метод:", self.action_input)
        form_layout.addRow("Голосовой ответ:", self.response_input)
        
        layout.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить команду")
        self.save_btn.clicked.connect(self.save_command)
        self.delete_btn = QPushButton("Удалить команду")
        self.delete_btn.clicked.connect(self.delete_command)
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def refresh_list(self):
        self.command_list.clear()
        commands = self.jarvis.config.get("commands", [])
        for cmd in commands:
            item = QListWidgetItem(f"{cmd['phrase']} -> {cmd['action']}")
            item.setData(100, cmd)
            self.command_list.addItem(item)

    def load_command(self, item):
        cmd = item.data(100)
        self.phrase_input.setText(cmd["phrase"])
        self.action_input.setText(cmd["action"])
        self.response_input.setText(cmd.get("response", ""))

    def save_command(self):
        phrase = self.phrase_input.text()
        action = self.action_input.text()
        response = self.response_input.text()
        
        if not phrase or not action:
            return
            
        commands = self.jarvis.config.get("commands", [])
        updated = False
        for cmd in commands:
            if cmd["phrase"] == phrase:
                cmd["action"] = action
                cmd["response"] = response
                updated = True
                break
        
        if not updated:
            commands.append({"phrase": phrase, "action": action, "response": response})
            
        self.jarvis.config.set("commands", commands)
        self.refresh_list()
        logger.info(f"Команда '{phrase}' сохранена через GUI.")

    def delete_command(self):
        phrase = self.phrase_input.text()
        commands = self.jarvis.config.get("commands", [])
        commands = [cmd for cmd in commands if cmd["phrase"] != phrase]
        self.jarvis.config.set("commands", commands)
        self.refresh_list()
        self.phrase_input.clear()
        self.action_input.clear()
        self.response_input.clear()
        logger.info(f"Команда '{phrase}' удалена через GUI.")
