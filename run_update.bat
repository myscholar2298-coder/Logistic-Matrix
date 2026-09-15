@echo off
cd /d "%~dp0"
C:\Users\SERVER\AppData\Local\Python\pythoncore-3.14-64\python.exe AutoUpdate.py || exit /b 1
C:\Users\SERVER\AppData\Local\Python\pythoncore-3.14-64\python.exe backend_sync.py || exit /b 1