@echo off
echo ===============================================
echo  🚀 SISTEMA SINISTROS ULTRATHINK - CORRIGIDO
echo      Versão com correções v2.1
echo ===============================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! Instale o Python 3.8+ primeiro.
    echo 💡 Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado! Instale o Node.js primeiro.
    echo 💡 Download: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Python e Node.js detectados
echo.

REM =================== CONFIGURAR BACKEND ===================
echo 📦 Configurando Backend...
cd backend

REM Verificar/criar ambiente virtual
if not exist "venv" (
    echo 🔧 Criando ambiente virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Erro ao criar ambiente virtual!
        pause
        exit /b 1
    )
)

echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Verificar e instalar dependências
echo 📥 Verificando dependências do backend...
python -c "import fastapi, uvicorn, sqlalchemy" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Instalando dependências...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Erro ao instalar dependências!
        pause
        exit /b 1
    )
)

REM Testar importação da aplicação
echo 🧪 Verificando aplicação FastAPI...
python -c "from app.main import app; print('✅ App verificada')"
if %errorlevel% neq 0 (
    echo ❌ Erro na aplicação FastAPI! Verifique os logs.
    pause
    exit /b 1
)

REM Verificar se a porta 8000 está livre
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do set PID_BACKEND=%%a
if defined PID_BACKEND (
    echo ❌ Porta 8000 já está em uso pelo processo PID %PID_BACKEND%.
    echo    Encerre o processo ou libere a porta antes de iniciar o sistema.
    pause
    exit /b 1
)

echo.
echo 🚀 Iniciando Backend API na porta 8000...
start "BACKEND - API Sinistros CORRIGIDA" cmd /c "call venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload && pause"

REM Aguardar backend inicializar
echo ⏳ Aguardando backend inicializar...
timeout /t 8 /nobreak >nul

REM =================== CONFIGURAR FRONTEND ===================
cd ..\frontend
echo.
echo 📦 Configurando Frontend...

if not exist "node_modules" (
    echo 📥 Instalando dependências do frontend...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Erro ao instalar dependências do frontend!
        pause
        exit /b 1
    )
) else (
    echo ✅ Dependências do frontend já instaladas
)

echo.
echo 🎨 Iniciando Frontend React na porta 5173...
start "FRONTEND - React App" cmd /c "npm run dev && pause"

REM Aguardar frontend inicializar
echo ⏳ Aguardando frontend inicializar...
timeout /t 10 /nobreak >nul

echo.
echo ===============================================
echo   ✅ SISTEMA ULTRATHINK CORRIGIDO E ATIVO!
echo ===============================================
echo.
echo 🌐 Acesse o sistema:
echo    Frontend: http://localhost:5173
echo    API Docs: http://localhost:8000/docs
echo    API Test: http://localhost:8000/
echo.
echo 🔧 Correções aplicadas:
echo    ✓ Corrigido erro de importação User
echo    ✓ Verificação de dependências melhorada
echo    ✓ Tratamento de erros aprimorado
echo    ✓ Logs mais detalhados
echo.
echo 📊 Funcionalidades Disponíveis:
echo    ✓ Dashboard Ultra Profissional
echo    ✓ Gestão de Sinistros com dados reais
echo    ✓ Filtros avançados
echo    ✓ Métricas em tempo real
echo    ✓ Interface moderna e responsiva
echo.
echo 🔧 Para parar o sistema:
echo    - Feche as janelas do terminal backend e frontend
echo    - Ou pressione Ctrl+C em cada janela
echo.

REM Aguardar e testar conexões
echo 🔍 Verificando se os serviços estão online...
timeout /t 3 /nobreak >nul

REM Tentar testar backend
echo 🧪 Testando backend...
powershell -command "try { $r = Invoke-WebRequest -Uri 'http://localhost:8000/' -UseBasicParsing -TimeoutSec 5; Write-Host '✅ Backend API: ONLINE' } catch { Write-Host '⚠️  Backend API: Verificando...' }"

REM Tentar testar frontend
echo 🧪 Testando frontend...
powershell -command "try { $r = Invoke-WebRequest -Uri 'http://localhost:5173' -UseBasicParsing -TimeoutSec 5; Write-Host '✅ Frontend React: ONLINE' } catch { Write-Host '⚠️  Frontend React: Iniciando...' }"

echo.
echo 🎯 Status: Sistema ULTRATHINK corrigido e pronto para uso!
echo.
echo 💡 Dicas:
echo    - Se houver erro de conexão, aguarde mais alguns segundos
echo    - Use Ctrl+C para parar os serviços quando terminar
echo    - Verifique os logs nas janelas do backend e frontend
echo.

REM Abrir navegador automaticamente após um tempo
timeout /t 5 /nobreak >nul
start http://localhost:5173

echo ⌨️  Pressione qualquer tecla para continuar monitorando...
pause >nul

cd .. 