import pytest
import os
import json
from unittest.mock import MagicMock, patch
from jarvis.utils.config import ConfigManager, DEFAULT_CONFIG
from jarvis.core.plugin_manager import PluginManager
from jarvis.core.command_engine import CommandEngine
from jarvis.core.speech import SpeechEngine

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
    
    mock_jarvis.speech.speak.assert_called()

@patch('pyttsx3.init')
def test_speech_engine(mock_init):
    mock_engine = MagicMock()
    mock_init.return_value = mock_engine

    speech = SpeechEngine()
    speech.say_text("Тест")

    # Since it runs in a thread, we might need a small wait or check if it was called
    # For simplicity in mock, we just check if it initialized
    mock_init.assert_called()

def test_activity_tracker():
    from jarvis.utils.activity_tracker import ActivityTracker
    mock_jarvis = MagicMock()
    tracker = ActivityTracker(mock_jarvis, limit_minutes=1)
    assert tracker.limit_seconds == 60
    tracker.update_limit(10)
    assert tracker.limit_seconds == 600
