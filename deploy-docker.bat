@echo off
REM Script de Deploy Docker - Sistema de Sinistros BRSAMOR (Windows)
REM Execute com: deploy-docker.bat

echo 🐋 Iniciando Deploy Docker...
echo ==================================

REM Verificar se Docker está rodando
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker não está rodando. Inicie o Docker primeiro.
    pause
    exit /b 1
)

REM Verificar se arquivo .env existe
if not exist "docker\.env" (
    echo ⚠️  Arquivo .env não encontrado. Copiando exemplo...
    copy "docker\.env.example" "docker\.env"
    echo 📝 Configure o arquivo docker\.env com suas credenciais antes de continuar.
    pause
    exit /b 1
)

echo 🔧 Parando containers existentes...
docker-compose down

echo 🏗️  Construindo imagens...
docker-compose build --no-cache

echo 🚀 Iniciando serviços...
docker-compose up -d

echo ⏳ Aguardando serviços ficarem prontos...
timeout /t 30 /nobreak >nul

echo 🔍 Verificando status dos serviços...

REM Verificar Backend
curl -f http://localhost:8001/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend: Falhou ao iniciar
) else (
    echo ✅ Backend: http://localhost:8001 - OK
)

REM Verificar Frontend
curl -f http://localhost/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Frontend: Falhou ao iniciar
) else (
    echo ✅ Frontend: http://localhost - OK
)

echo.
echo 🎯 Deploy concluído!
echo ==================================
echo 📊 Acessos:
echo    Frontend: http://localhost
echo    Backend:  http://localhost:8001
echo    API Docs: http://localhost:8001/docs
echo.
echo 📋 Comandos úteis:
echo    Ver logs:     docker-compose logs -f
echo    Parar:        docker-compose down
echo    Reiniciar:    docker-compose restart
echo    Status:       docker-compose ps
echo ==================================
pause 