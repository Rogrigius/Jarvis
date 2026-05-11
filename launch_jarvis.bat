@echo off
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
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Запуск приложения
echo Запуск ДЖАРВИСА...
python main.py

pause
