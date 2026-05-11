import os
import sys
from jarvis_voice.utils.logger import logger

def add_to_startup():
    """Adds the application to Windows Startup."""
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "JARVIS", 0, winreg.REG_SZ, sys.argv[0])
            logger.info("Добавлено в автозагрузку Windows.")
            return True
        except Exception as e:
            logger.error(f"Не удалось добавить в автозагрузку: {e}")
            return False
    else:
        logger.warning("Автозагрузка поддерживается только для Windows.")
        return False

def remove_from_startup():
    """Removes the application from Windows Startup."""
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.DeleteValue(reg_key, "JARVIS")
            logger.info("Удалено из автозагрузки Windows.")
            return True
        except Exception as e:
            logger.error(f"Не удалось удалить из автозагрузки: {e}")
            return False
    return False
