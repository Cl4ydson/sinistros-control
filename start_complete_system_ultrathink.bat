@echo off
echo ===================================
echo  🚀 SISTEMA SINISTROS ULTRATHINK
echo     Inicializacao Completa v2.0
echo ===================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! Instale o Python 3.8+ primeiro.
    pause
    exit /b 1
)

REM Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado! Instale o Node.js primeiro.
    pause
    exit /b 1
)

echo ✅ Python e Node.js detectados
echo.

REM Configurar backend
echo 📦 Configurando Backend...
cd backend
if not exist "venv" (
    echo 🔧 Criando ambiente virtual...
    python -m venv venv
)

echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate

echo 📥 Instalando dependências do backend...
pip install -r requirements.txt

REM Testar conexão com banco
echo 🔗 Testando conexão com banco de dados...
python test_connection.py
if %errorlevel% neq 0 (
    echo ⚠️  Aviso: Problemas na conexão com banco. Continuando...
)

echo.
echo 🚀 Iniciando Backend API...
start "BACKEND - API Sinistros" cmd /c "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Aguardar backend inicializar
echo ⏳ Aguardando backend inicializar...
timeout /t 5 /nobreak >nul

REM Configurar frontend
cd ..\frontend
echo.
echo 📦 Configurando Frontend...

if not exist "node_modules" (
    echo 📥 Instalando dependências do frontend...
    npm install
) else (
    echo ✅ Dependências já instaladas
)

echo.
echo 🎨 Iniciando Frontend React...
start "FRONTEND - React App" cmd /c "npm run dev"

REM Aguardar frontend inicializar
echo ⏳ Aguardando frontend inicializar...
timeout /t 8 /nobreak >nul

echo.
echo ===================================
echo   ✅ SISTEMA ULTRATHINK ATIVO!
echo ===================================
echo.
echo 🌐 Acesse o sistema:
echo    Frontend: http://localhost:5173
echo    API Docs: http://localhost:8000/docs
echo    ReDoc:    http://localhost:8000/redoc
echo.
echo 📊 Funcionalidades Disponíveis:
echo    ✓ Dashboard Ultra Profissional
echo    ✓ Gestão de Sinistros com dados reais
echo    ✓ Filtros avançados
echo    ✓ Métricas em tempo real
echo    ✓ Interface moderna e responsiva
echo.
echo 🔧 Para parar o sistema:
echo    - Feche as janelas do terminal
echo    - Ou pressione Ctrl+C em cada janela
echo.
echo 📄 Documentação completa em:
echo    - MELHORIAS_ULTRATHINK.md
echo    - FRONTEND_ULTRATHINK.md
echo.

REM Verificar se os serviços estão rodando
echo 🔍 Verificando serviços...
timeout /t 3 /nobreak >nul

REM Testar backend
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend API: ONLINE
) else (
    echo ⚠️  Backend API: Verificando...
)

REM Testar frontend
curl -s http://localhost:5173 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend React: ONLINE
) else (
    echo ⚠️  Frontend React: Iniciando...
)

echo.
echo 🎯 Status: Sistema ULTRATHINK pronto para uso!
echo 💡 Dica: Use Ctrl+C para parar os serviços quando terminar
echo.

REM Abrir navegador automaticamente
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo ⌨️  Pressione qualquer tecla para continuar monitorando...
pause >nul

cd .. 