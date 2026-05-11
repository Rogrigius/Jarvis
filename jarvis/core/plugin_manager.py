import importlib
import os
import inspect
from jarvis.utils.logger import logger
from jarvis.plugins.plugin_base import PluginBase

class PluginManager:
    def __init__(self, jarvis_context, plugin_dir="jarvis/plugins"):
        self.jarvis = jarvis_context
        self.plugin_dir = plugin_dir
        self.plugins = []
        self.command_map = {}

    def load_plugins(self):
        if not os.path.exists(self.plugin_dir):
            logger.warning(f"Plugin directory {self.plugin_dir} not found.")
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith("_plugin.py") and filename != "plugin_base.py":
                module_name = f"jarvis.plugins.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, PluginBase) and obj is not PluginBase:
                            plugin_instance = obj(self.jarvis)
                            self.plugins.append(plugin_instance)
                            self.command_map.update(plugin_instance.get_commands())
                            logger.info(f"Loaded plugin: {name} from {filename}")
                except Exception as e:
                    logger.error(f"Failed to load plugin from {filename}: {e}")

    def execute_plugin_command(self, action_name, *args, **kwargs):
        for plugin in self.plugins:
            if hasattr(plugin, action_name):
                method = getattr(plugin, action_name)
                return method(*args, **kwargs)
        return None
