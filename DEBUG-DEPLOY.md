# 🔧 Debug de Deploy - Soluções para Problemas Comuns

## 🔺 Problema 1: Vercel - "Project already exists"

### **Erro:**
```
Project "sinistros-control" already exists, please use a new name.
```

### **Solução:**
✅ **Usar nome único para o projeto**

```bash
# Opção 1: Usar script corrigido
./deploy-vercel-fix.sh

# Opção 2: Deploy manual com nome único
vercel --name sinistros-brsamor-2025 --prod

# Opção 3: Limpar e recriar
rm -rf .vercel
vercel --prod
```

### **Arquivo atualizado:**
- ✅ `vercel.json` - nome alterado para `sinistros-brsamor-2025`
- ✅ URL será: `https://sinistros-brsamor-2025.vercel.app`

---

## 🐋 Problema 2: Docker - Erro de Import

### **Erro:**
```
ModuleNotFoundError: No module named 'app'
ImportError: cannot import name 'main' from 'app.main'
```

### **Causa:**
- ❌ PYTHONPATH não configurado corretamente
- ❌ Estrutura de diretórios não reconhecida como pacote Python
- ❌ Imports relativos não funcionando

### **Soluções Implementadas:**

#### **1. PYTHONPATH Corrigido:**
```dockerfile
# Dockerfile
ENV PYTHONPATH=/app:/app/backend
```

```yaml
# docker-compose.yml
environment:
  - PYTHONPATH=/app:/app/backend
```

#### **2. Arquivo __init__.py:**
```python
# backend/__init__.py (criado)
# Arquivo para tornar o diretório backend um pacote Python válido
```

#### **3. Scripts Corrigidos:**
- ✅ `deploy-docker-fix.sh` - versão Linux/Mac
- ✅ `deploy-docker-fix.bat` - versão Windows
- ✅ Logs detalhados para debugging
- ✅ Limpeza de containers/imagens antigas

### **Como usar:**
```bash
# Windows
deploy-docker-fix.bat

# Linux/Mac
chmod +x deploy-docker-fix.sh
./deploy-docker-fix.sh
```

---

## 🔍 Debug Avançado

### **Docker - Verificar Logs:**
```bash
# Logs gerais
docker-compose logs -f

# Logs só do backend
docker-compose logs backend

# Entrar no container para debug
docker-compose exec backend bash

# Testar imports dentro do container
docker-compose exec backend python -c "from app.main import app; print('Import OK')"
```

### **Vercel - Verificar Configuração:**
```bash
# Ver projetos existentes
vercel list

# Ver logs de deploy
vercel logs sinistros-brsamor-2025

# Abrir dashboard
vercel dashboard

# Redeployar
vercel --prod
```

---

## 🎯 Checklist de Verificação

### **Antes do Deploy Docker:**
- [ ] Docker Desktop está rodando
- [ ] Arquivo `docker/.env` configurado com credenciais
- [ ] Portas 80 e 8001 livres
- [ ] Espaço em disco suficiente (2GB+)

### **Antes do Deploy Vercel:**
- [ ] Vercel CLI instalado (`npm install -g vercel`)
- [ ] Login feito (`vercel login`)
- [ ] Projeto frontend buildável (`cd frontend && npm run build`)
- [ ] Variáveis de ambiente configuradas no dashboard

---

## 🚨 Soluções Rápidas

### **Docker não inicia:**
```bash
# Limpar tudo e recomeçar
docker-compose down --remove-orphans
docker system prune -a
./deploy-docker-fix.sh
```

### **Vercel erro de nome:**
```bash
# Usar nome único
rm -rf .vercel
vercel --name meu-projeto-$(date +%s) --prod
```

### **Import error persistente:**
```bash
# Verificar estrutura dentro do container
docker-compose exec backend ls -la /app/
docker-compose exec backend python -c "import sys; print(sys.path)"
```

---

## 📞 Suporte Adicional

Se os problemas persistirem:

1. **Execute os scripts corrigidos** (`deploy-*-fix.*`)
2. **Copie os logs completos** dos comandos
3. **Verifique as configurações** nos arquivos `.env`
4. **Use o checklist** de verificação acima

### **Logs Importantes:**
```bash
# Docker
docker-compose logs backend > backend-logs.txt
docker-compose logs frontend > frontend-logs.txt

# Vercel
vercel logs [url] > vercel-logs.txt
```

---

<div align="center">

**🔧 Problemas resolvidos! Use os scripts corrigidos para deploy sem erros.**

[![Docker Fix](https://img.shields.io/badge/Docker-Fixed-green?logo=docker)](./deploy-docker-fix.sh)
[![Vercel Fix](https://img.shields.io/badge/Vercel-Fixed-black?logo=vercel)](./deploy-vercel-fix.sh)

</div> 