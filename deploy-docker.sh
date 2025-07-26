#!/bin/bash

# Script de Deploy Docker - Sistema de Sinistros BRSAMOR
# Execute com: ./deploy-docker.sh

echo "🐋 Iniciando Deploy Docker..."
echo "=================================="

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

# Verificar se arquivo .env existe
if [ ! -f "docker/.env" ]; then
    echo "⚠️  Arquivo .env não encontrado. Copiando exemplo..."
    cp docker/.env.example docker/.env
    echo "📝 Configure o arquivo docker/.env com suas credenciais antes de continuar."
    exit 1
fi

echo "🔧 Parando containers existentes..."
docker-compose down

echo "🏗️  Construindo imagens..."
docker-compose build --no-cache

echo "🚀 Iniciando serviços..."
docker-compose up -d

echo "⏳ Aguardando serviços ficarem prontos..."
sleep 30

# Verificar saúde dos serviços
echo "🔍 Verificando status dos serviços..."

# Backend
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Backend: http://localhost:8001 - OK"
else
    echo "❌ Backend: Falhou ao iniciar"
fi

# Frontend  
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Frontend: http://localhost - OK"
else
    echo "❌ Frontend: Falhou ao iniciar"
fi

echo ""
echo "🎯 Deploy concluído!"
echo "=================================="
echo "📊 Acessos:"
echo "   Frontend: http://localhost"
echo "   Backend:  http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo ""
echo "📋 Comandos úteis:"
echo "   Ver logs:     docker-compose logs -f"
echo "   Parar:        docker-compose down"
echo "   Reiniciar:    docker-compose restart"
echo "   Status:       docker-compose ps"
echo "==================================" 