class PluginBase:
    def __init__(self, jarvis_context):
        self.jarvis = jarvis_context

    def get_commands(self):
        """Returns a dict of {phrase: method_name}"""
        return {}
