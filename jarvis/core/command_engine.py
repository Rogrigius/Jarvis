from jarvis.utils.logger import logger

class CommandEngine:
    def __init__(self, jarvis_context):
        self.jarvis = jarvis_context

    def process_text(self, text):
        if not text:
            return

        logger.info(f"Processing text: {text}")
        
        # 1. Check custom commands from config
        config_commands = self.jarvis.config.get("commands", [])
        for cmd in config_commands:
            if cmd["phrase"] in text:
                logger.info(f"Matched config command: {cmd['phrase']}")
                self.execute_action(cmd["action"], cmd.get("response"))
                return

        # 2. Check plugin commands
        plugin_commands = self.jarvis.plugin_manager.command_map
        for phrase, action_name in plugin_commands.items():
            if phrase in text:
                logger.info(f"Matched plugin command: {phrase}")
                self.execute_plugin_action(action_name)
                return

        # 3. Handle unknown command
        logger.warning(f"Unknown command: {text}")
        # Could integrate an AI model here in the future

    def execute_action(self, action, response_template):
        if action == "greet":
            self.jarvis.speech.speak(response_template)
        elif action == "get_time":
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M")
            response = response_template.format(time=current_time)
            self.jarvis.speech.speak(response)
        else:
            # Try to see if it's a plugin action even if defined in config
            if not self.execute_plugin_action(action):
                if response_template:
                    self.jarvis.speech.speak(response_template)

    def execute_plugin_action(self, action_name):
        return self.jarvis.plugin_manager.execute_plugin_command(action_name)
