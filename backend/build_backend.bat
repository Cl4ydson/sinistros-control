@echo off
REM Gera executável único back-end
py -m pip install -r backend/requirements.txt
py -m PyInstaller backend/app/main.py --onefile --name backend

REM Instruções rápidas
REM   1. Executar este .bat
REM   2. O arquivo dist\backend.exe é o servidor local (porta 8000)
