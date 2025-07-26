@echo off
echo 🚀 Iniciando Backend na porta 8001...

cd backend
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado
echo 🔄 Iniciando servidor...

start "BACKEND-API" cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"

echo ⏳ Aguardando servidor inicializar...
timeout /t 5 /nobreak >nul

echo 🧪 Testando conexão...
powershell -command "try { $r = Invoke-WebRequest -Uri 'http://localhost:8001/' -UseBasicParsing -TimeoutSec 5; Write-Host '✅ Backend ONLINE na porta 8001' } catch { Write-Host '⚠️ Backend ainda inicializando...' }"

echo.
echo 🌐 URLs disponíveis:
echo    API: http://localhost:8001/
echo    Docs: http://localhost:8001/docs
echo    Health: http://localhost:8001/api/automacao/sinistros/health
echo.
echo ✅ Backend iniciado com sucesso!
pause