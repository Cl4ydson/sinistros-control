#!/bin/bash

# Script de Deploy Vercel - Sistema de Sinistros BRSAMOR (CORRIGIDO)
# Execute com: ./deploy-vercel-fix.sh

echo "🔺 Iniciando Deploy Vercel (CORRIGIDO)..."
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

# Limpar projetos existentes (se necessário)
echo "🧹 Limpando configurações anteriores..."
rm -rf .vercel

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

# Deploy com nome único
echo "🚀 Fazendo deploy com nome único..."
vercel --name sinistros-brsamor-2025 --prod

echo ""
echo "🎯 Deploy concluído!"
echo "=================================="
echo "📊 Próximos passos:"
echo "   1. Configure as variáveis de ambiente no dashboard Vercel"
echo "   2. URL será: https://sinistros-brsamor-2025.vercel.app"
echo "   3. Teste a aplicação na URL fornecida"
echo ""
echo "📋 Comandos úteis:"
echo "   Ver logs:     vercel logs sinistros-brsamor-2025"
echo "   Dashboard:    vercel dashboard"
echo "   Redeploy:     vercel --prod"
echo "==================================" 