# 🚀 Guia de Deploy - Sistema de Sinistros BRSAMOR

Este guia apresenta duas opções de deploy para o sistema: **Docker** (containerizado) e **Vercel** (serverless).

## 📋 Índice

- [🐋 Deploy com Docker](#-deploy-com-docker)
- [🔺 Deploy com Vercel](#-deploy-com-vercel)
- [⚖️ Comparação das Opções](#️-comparação-das-opções)
- [🔧 Troubleshooting](#-troubleshooting)

---

## 🐋 Deploy com Docker

### **Vantagens**
- ✅ **Controle Total**: Ambiente isolado e controlado
- ✅ **Desenvolvimento Local**: Replica produção localmente
- ✅ **Banco PyODBC**: Suporte completo ao SQL Server
- ✅ **Recursos**: Sem limitações de CPU/memória
- ✅ **Debugging**: Logs completos e acesso direto

### **Desvantagens**
- ❌ **Infraestrutura**: Precisa gerenciar servidor
- ❌ **Custos**: Servidor sempre rodando
- ❌ **Manutenção**: Updates e patches manuais

### **Pré-requisitos**
```bash
# Instalar Docker
- Docker Desktop (Windows/Mac)
- Docker Engine (Linux)

# Verificar instalação
docker --version
docker-compose --version
```

### **Configuração**

#### **1. Configurar Variáveis de Ambiente**
```bash
# Copiar exemplo
cp docker/.env.example docker/.env

# Editar com suas credenciais
nano docker/.env
```

```env
# docker/.env
DB_SERVER=SRVTOTVS02
DB_DATABASE=AUTOMACAO_BRSAMOR
DB_USERNAME=adm
DB_PASSWORD=sua_senha_segura

SECRET_KEY=chave_jwt_super_secreta_32_caracteres_ou_mais
```

#### **2. Deploy Automático**
```bash
# Windows
deploy-docker.bat

# Linux/Mac
chmod +x deploy-docker.sh
./deploy-docker.sh
```

#### **3. Deploy Manual**
```bash
# Construir imagens
docker-compose build --no-cache

# Iniciar serviços
docker-compose up -d

# Verificar status
docker-compose ps
```

### **Acessos**
- **🌐 Frontend**: http://localhost
- **🔗 Backend**: http://localhost:8001
- **📚 API Docs**: http://localhost:8001/docs

### **Gerenciamento**
```bash
# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Reiniciar
docker-compose restart

# Atualizar
git pull
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔺 Deploy com Vercel

### **Vantagens**
- ✅ **Serverless**: Escala automaticamente
- ✅ **Custo Zero**: Tier gratuito generoso
- ✅ **CDN Global**: Performance mundial
- ✅ **CI/CD**: Deploy automático do Git
- ✅ **HTTPS**: SSL/TLS automático

### **Desvantagens**
- ❌ **Limitações**: Timeout de 30s por função
- ❌ **Banco**: PyODBC não funciona (precisa adaptação)
- ❌ **Cold Start**: Primeiro request mais lento
- ❌ **Debugging**: Logs limitados

### **Pré-requisitos**
```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login
```

### **Configuração**

#### **1. Adaptar Backend para Serverless**
O backend precisará ser adaptado para funcionar sem PyODBC:

```python
# Use SQLAlchemy com um driver compatível
# Substitua pyodbc por pymssql ou similar
pip install pymssql
```

#### **2. Configurar Variáveis no Dashboard**
Acesse [vercel.com/dashboard](https://vercel.com/dashboard) e configure:

```env
DB_SERVER=SRVTOTVS02
DB_DATABASE=AUTOMACAO_BRSAMOR
DB_USERNAME=adm
DB_PASSWORD=sua_senha_segura
SECRET_KEY=chave_jwt_super_secreta
```

#### **3. Deploy Automático**
```bash
# Executar script
chmod +x deploy-vercel.sh
./deploy-vercel.sh

# Ou manual
vercel --prod
```

#### **4. Atualizar URLs**
Edite `vercel.json` com sua URL real:
```json
{
  "build": {
    "env": {
      "VITE_API_BASE_URL": "https://sua-app.vercel.app"
    }
  }
}
```

### **Acessos**
- **🌐 Aplicação**: https://sua-app.vercel.app
- **📊 Dashboard**: https://vercel.com/dashboard
- **📈 Analytics**: Automático no dashboard

### **Gerenciamento**
```bash
# Redeploy
vercel --prod

# Ver logs
vercel logs https://sua-app.vercel.app

# Dashboard
vercel dashboard
```

---

## ⚖️ Comparação das Opções

| Critério | Docker | Vercel |
|----------|--------|--------|
| **Custo** | Servidor pago | Gratuito até 100GB |
| **Performance** | Alta, dedicada | Boa, com cold start |
| **Escalabilidade** | Manual | Automática |
| **Manutenção** | Alta | Baixa |
| **Banco PyODBC** | ✅ Suportado | ❌ Requer adaptação |
| **Controle** | Total | Limitado |
| **Setup** | Médio | Fácil |
| **Produção** | Empresarial | Pequeno/Médio |

## 🎯 Recomendações

### **Use Docker quando:**
- ✅ Ambiente empresarial
- ✅ Precisa do PyODBC original
- ✅ Controle total necessário
- ✅ Recursos dedicados importantes
- ✅ Integrações complexas

### **Use Vercel quando:**
- ✅ Projeto pessoal/startup
- ✅ Orçamento limitado
- ✅ Tráfego variável
- ✅ Deploy rápido necessário
- ✅ Manutenção mínima

---

## 🔧 Troubleshooting

### **Docker Issues**

#### **Erro: Port already in use**
```bash
# Parar processos conflitantes
docker-compose down
sudo lsof -i :8001
sudo kill -9 [PID]
```

#### **Erro: Database connection**
```bash
# Verificar variáveis
cat docker/.env

# Testar conexão
docker-compose exec backend python -c "from app.database import test_connection; test_connection()"
```

#### **Erro: Build failed**
```bash
# Limpar cache
docker system prune -a
docker-compose build --no-cache
```

### **Vercel Issues**

#### **Erro: Function timeout**
```bash
# Otimizar queries
# Implementar cache
# Dividir em múltiplas funções
```

#### **Erro: Database driver**
```bash
# Substituir PyODBC
pip uninstall pyodbc
pip install pymssql

# Atualizar connection string
# mssql+pymssql://user:pass@server/db
```

#### **Erro: Environment variables**
```bash
# Verificar no dashboard
vercel env ls

# Adicionar via CLI
vercel env add DB_SERVER
```

### **Geral**

#### **Erro: CORS**
```python
# Backend: app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### **Erro: API not found**
```bash
# Verificar rotas
curl -f http://localhost:8001/docs

# Verificar proxy nginx
cat frontend/nginx.conf
```

---

## 📞 Suporte

Para problemas específicos:

- **🐋 Docker**: [Docker Documentation](https://docs.docker.com/)
- **🔺 Vercel**: [Vercel Documentation](https://vercel.com/docs)
- **🎯 Sistema**: Abra uma issue no repositório

---

<div align="center">

**🚀 Ambas as opções são válidas - escolha a que melhor se adequa ao seu caso!**

</div> 