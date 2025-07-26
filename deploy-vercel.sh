#!/bin/bash

# Script de Deploy Vercel - Sistema de Sinistros BRSAMOR
# Execute com: ./deploy-vercel.sh

echo "🔺 Iniciando Deploy Vercel..."
echo "=================================="

# Verificar se Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI não encontrado. Instalando..."
    npm install -g vercel
fi

# Verificar se está logado no Vercel
if ! vercel whoami > /dev/null 2>&1; then
    echo "🔐 Fazendo login no Vercel..."
    vercel login
fi

# Preparar frontend para build
echo "🏗️  Preparando frontend..."
cd frontend
npm install
npm run build
cd ..

echo "📝 Configurando variáveis de ambiente..."
echo "⚠️  Configure as seguintes variáveis no dashboard da Vercel:"
echo "   DB_SERVER"
echo "   DB_DATABASE" 
echo "   DB_USERNAME"
echo "   DB_PASSWORD"
echo "   SECRET_KEY"
echo ""

# Deploy
echo "🚀 Fazendo deploy..."
vercel --prod

echo ""
echo "🎯 Deploy concluído!"
echo "=================================="
echo "📊 Próximos passos:"
echo "   1. Configure as variáveis de ambiente no dashboard Vercel"
echo "   2. Atualize VITE_API_BASE_URL no vercel.json com sua URL"
echo "   3. Teste a aplicação na URL fornecida"
echo ""
echo "📋 Comandos úteis:"
echo "   Ver logs:     vercel logs [url]"
echo "   Dashboard:    vercel dashboard"
echo "   Redeploy:     vercel --prod"
echo "==================================" 