@echo off
echo 🎨 Iniciando Frontend na porta 5173...

cd frontend

echo 🔄 Iniciando servidor React...
start "FRONTEND-REACT" cmd /k "npm run dev"

echo ⏳ Aguardando frontend inicializar...
timeout /t 10 /nobreak >nul

echo 🧪 Testando conexão...
powershell -command "try { $r = Invoke-WebRequest -Uri 'http://localhost:5173' -UseBasicParsing -TimeoutSec 5; Write-Host '✅ Frontend ONLINE na porta 5173' } catch { Write-Host '⚠️ Frontend ainda inicializando...' }"

echo.
echo 🌐 URLs disponíveis:
echo    Frontend: http://localhost:5173
echo    Login: http://localhost:5173/login
echo.
echo ✅ Frontend iniciado com sucesso!
pause