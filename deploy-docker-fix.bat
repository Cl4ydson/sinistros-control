@echo off
REM Script de Deploy Docker - Sistema de Sinistros BRSAMOR (CORRIGIDO - Windows)
REM Execute com: deploy-docker-fix.bat

echo 🐋 Iniciando Deploy Docker (CORRIGIDO)...
echo ==================================

REM Verificar se Docker está rodando
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker não está rodando. Inicie o Docker primeiro.
    pause
    exit /b 1
)

REM Criar arquivo .env se não existir
if not exist "docker\.env" (
    echo 📁 Criando diretório docker...
    mkdir docker 2>nul
    
    echo ⚠️  Criando arquivo .env básico...
    (
        echo # Configurações de Banco de Dados
        echo DB_SERVER=SRVTOTVS02
        echo DB_DATABASE=AUTOMACAO_BRSAMOR
        echo DB_USERNAME=adm
        echo DB_PASSWORD=sua_senha_aqui
        echo.
        echo # Configurações de Segurança
        echo SECRET_KEY=sua_chave_secreta_muito_forte_aqui_com_32_caracteres_ou_mais
        echo ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=30
        echo.
        echo # Configurações de Ambiente
        echo ENVIRONMENT=production
        echo DEBUG=false
    ) > docker\.env
    
    echo 📝 Configure o arquivo docker\.env com suas credenciais antes de continuar.
    pause
)

echo 🔧 Parando containers existentes...
docker-compose down --remove-orphans

echo 🧹 Limpando imagens antigas...
docker system prune -f

echo 🏗️  Construindo imagens (corrigido para imports)...
docker-compose build --no-cache

echo 🚀 Iniciando serviços...
docker-compose up -d

echo ⏳ Aguardando serviços ficarem prontos...
timeout /t 45 /nobreak >nul

echo 🔍 Verificando status dos serviços...

REM Verificar Backend
echo 🔧 Testando backend...
curl -f http://localhost:8001/health >nul 2>&1
if errorlevel 1 (
    curl -f http://localhost:8001/docs >nul 2>&1
    if errorlevel 1 (
        echo ❌ Backend: Verificando logs...
        docker-compose logs backend
    ) else (
        echo ✅ Backend: http://localhost:8001 - OK (docs disponível)
    )
) else (
    echo ✅ Backend: http://localhost:8001 - OK
)

REM Verificar Frontend
curl -f http://localhost/health >nul 2>&1
if errorlevel 1 (
    curl -f http://localhost/ >nul 2>&1
    if errorlevel 1 (
        echo ❌ Frontend: Verificando logs...
        docker-compose logs frontend
    ) else (
        echo ✅ Frontend: http://localhost - OK
    )
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
echo    Ver logs backend: docker-compose logs backend
echo    Parar:        docker-compose down
echo    Reiniciar:    docker-compose restart
echo    Status:       docker-compose ps
echo    Entrar no container: docker-compose exec backend bash
echo ==================================
pause 