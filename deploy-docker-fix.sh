#!/bin/bash

# Script de Deploy Docker - Sistema de Sinistros BRSAMOR (CORRIGIDO)
# Execute com: ./deploy-docker-fix.sh

echo "🐋 Iniciando Deploy Docker (CORRIGIDO)..."
echo "=================================="

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

# Criar arquivo .env se não existir
if [ ! -f "docker/.env" ]; then
    echo "📁 Criando diretório docker..."
    mkdir -p docker
    
    echo "⚠️  Criando arquivo .env básico..."
    cat > docker/.env << 'EOF'
# Configurações de Banco de Dados
DB_SERVER=SRVTOTVS02
DB_DATABASE=AUTOMACAO_BRSAMOR
DB_USERNAME=adm
DB_PASSWORD=sua_senha_aqui

# Configurações de Segurança
SECRET_KEY=sua_chave_secreta_muito_forte_aqui_com_32_caracteres_ou_mais
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configurações de Ambiente
ENVIRONMENT=production
DEBUG=false
EOF
    
    echo "📝 Configure o arquivo docker/.env com suas credenciais antes de continuar."
    echo "Pressione ENTER após configurar..."
    read
fi

echo "🔧 Parando containers existentes..."
docker-compose down --remove-orphans

echo "🧹 Limpando imagens antigas..."
docker system prune -f

echo "🏗️  Construindo imagens (corrigido para imports)..."
docker-compose build --no-cache

echo "🚀 Iniciando serviços..."
docker-compose up -d

echo "⏳ Aguardando serviços ficarem prontos..."
sleep 45

# Verificar saúde dos serviços
echo "🔍 Verificando status dos serviços..."

# Verificar backend
echo "🔧 Testando backend..."
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Backend: http://localhost:8001 - OK"
elif curl -f http://localhost:8001/docs > /dev/null 2>&1; then
    echo "✅ Backend: http://localhost:8001 - OK (docs disponível)"
else
    echo "❌ Backend: Verificando logs..."
    docker-compose logs backend | tail -20
fi

# Verificar frontend
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Frontend: http://localhost - OK"
elif curl -f http://localhost/ > /dev/null 2>&1; then
    echo "✅ Frontend: http://localhost - OK"
else
    echo "❌ Frontend: Verificando logs..."
    docker-compose logs frontend | tail -10
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
echo "   Ver logs backend: docker-compose logs backend"
echo "   Parar:        docker-compose down"
echo "   Reiniciar:    docker-compose restart"
echo "   Status:       docker-compose ps"
echo "   Entrar no container: docker-compose exec backend bash"
echo "==================================" 