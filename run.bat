@echo off
cd /d "%~dp0"
echo Installing packages (first time only)...
pip install -r requirements.txt
echo.
echo Starting the chatbot...
python web_chatbot.py
pause
