import pytest
import os
import json
from unittest.mock import MagicMock
from jarvis.utils.config import ConfigManager, DEFAULT_CONFIG
from jarvis.core.plugin_manager import PluginManager
from jarvis.core.command_engine import CommandEngine

@pytest.fixture
def temp_config(tmp_path):
    config_file = tmp_path / "config.json"
    return str(config_file)

def test_config_manager_load_save(temp_config):
    cm = ConfigManager(config_path=temp_config)
    assert cm.get("name") == "ДЖАРВИС"
    
    cm.set("name", "ЭДИС")
    assert cm.get("name") == "ЭДИС"
    
    # Reload to verify persistence
    cm2 = ConfigManager(config_path=temp_config)
    assert cm2.get("name") == "ЭДИС"

def test_plugin_manager_loading():
    mock_jarvis = MagicMock()
    pm = PluginManager(mock_jarvis, plugin_dir="non_existent")
    pm.load_plugins()
    assert len(pm.plugins) == 0

def test_command_engine_processing():
    mock_jarvis = MagicMock()
    mock_jarvis.config.get.return_value = DEFAULT_CONFIG["commands"]
    mock_jarvis.plugin_manager.command_map = {}
    
    ce = CommandEngine(mock_jarvis)
    ce.process_text("привет")
    
    mock_jarvis.speech.speak.assert_called_with("Здравствуйте, сэр. Чем могу помочь?")
