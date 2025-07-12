@echo off
echo ===================================
echo      INICIANDO SERVIDOR BACKEND
echo ===================================

cd backend

echo Verificando Python...
python --version

echo.
echo Verificando se consegue importar a aplicacao...
python -c "from app.main import app; print('✓ App importada com sucesso!')"

echo.
echo Iniciando servidor na porta 8000...
python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1

pause 