@echo off
setlocal enabledelayedexpansion

:: Переход в директорию скрипта
cd /d "%~dp0"
echo Инициализация ДЖАРВИСА...

:: Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python не установлен. Пожалуйста, установите Python 3.10 или выше.
    pause
    exit /b
)

:: Создание виртуального окружения
if not exist "venv" (
    echo Создание виртуального окружения...
    python -m venv venv
)

:: Активация и установка зависимостей
echo Установка зависимостей...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Ошибка: не удалось найти venv\Scripts\activate.bat.
    pause
    exit /b
)

python -m pip install --upgrade pip
pip install -r requirements.txt

:: Установка PYTHONPATH для надежности (без лишних слешей)
set "PROJECT_ROOT=%~dp0"
if "!PROJECT_ROOT:~-1!"=="\" set "PROJECT_ROOT=!PROJECT_ROOT:~0,-1!"
set "PYTHONPATH=!PROJECT_ROOT!;!PYTHONPATH!"

:: Запуск приложения
echo Запуск ДЖАРВИСА...
python main.py

pause
