# 🚀 Guia de Deploy no Coolify - Sistema de Controle de Sinistros BRSAMOR

## 📋 Pré-requisitos

- ✅ VPS com Coolify instalado
- ✅ Domínio configurado (ex: `sinistros.seudominio.com.br`)
- ✅ Acesso aos servidores de banco de dados
- ✅ Repositório Git com o código

## 🔧 Configuração no Coolify

### 1. **Criar Novo Projeto**

1. Acesse o painel do Coolify
2. Clique em "New Project"
3. Nome: `Sistema de Sinistros BRSAMOR`
4. Descrição: `Sistema de controle de sinistros de transporte`

### 2. **Conectar Repositório**

1. Clique em "New Resource" → "Git Repository"
2. Conecte ao seu repositório Git
3. Branch: `main` ou `master`
4. Build Pack: `Docker Compose`
5. Docker Compose File: `docker-compose.yml`

### 3. **Configurar Variáveis de Ambiente**

No painel do Coolify, adicione as seguintes variáveis:

#### **🗄️ Banco de Dados Principal**
```env
DB_SERVER=SRVTOTVS02
DB_DATABASE=AUTOMACAO_BRSAMOR
DB_USERNAME=adm
DB_PASSWORD=(Br$amor#2020)
```

#### **🗄️ Banco de Dados Transporte**
```env
DB_TRANSPORT_SERVER=137.131.246.149
DB_TRANSPORT_DATABASE=dtbTransporte
DB_TRANSPORT_USERNAME=consulta.pbi
DB_TRANSPORT_PASSWORD=Br$Samor@2025#C
```

#### **🔐 Segurança**
```env
SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars-here
```
> ⚠️ **IMPORTANTE**: Gere uma chave secreta forte: `openssl rand -hex 32`

#### **🌐 Aplicação**
```env
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=*
TRUST_SERVER_CERTIFICATE=yes
ENCRYPT=no
VITE_API_BASE_URL=/api
VITE_DEMO_MODE=false
DOMAIN=sinistros.seudominio.com.br
PORT=80
```

### 4. **Configurar Domínio**

1. Vá para "Domains"
2. Adicione seu domínio: `sinistros.seudominio.com.br`
3. Ative "Generate SSL Certificate"
4. Configure DNS para apontar para o IP da VPS

### 5. **Configurar Rede**

1. Certifique-se de que a VPS pode acessar os servidores de banco:
   - `SRVTOTVS02` (porta 1433)
   - `137.131.246.149` (porta 1433)

2. Configure firewall se necessário:
   ```bash
   # Permitir conexões de saída para SQL Server
   ufw allow out 1433
   ```

## 🚀 Deploy

### 1. **Primeiro Deploy**

1. No painel do Coolify, clique em "Deploy"
2. Aguarde o build dos containers
3. Verifique os logs para erros

### 2. **Inicializar Dados**

Após o primeiro deploy bem-sucedido:

1. Acesse o container do backend:
   ```bash
   docker exec -it <container_name> python scripts/init_production.py
   ```

2. Ou execute via Coolify Console:
   ```bash
   cd /app && python scripts/init_production.py
   ```

### 3. **Verificar Funcionamento**

1. **Health Checks**:
   - Backend: `https://sinistros.seudominio.com.br/api/health`
   - Frontend: `https://sinistros.seudominio.com.br/health`

2. **API Documentation**:
   - `https://sinistros.seudominio.com.br/api/docs`

3. **Login**:
   - Acesse: `https://sinistros.seudominio.com.br`
   - Usuário: `admin`
   - Senha: `BrSamor@2025!`

## 🔍 Monitoramento

### **Logs**

No Coolify, monitore os logs:

1. **Backend Logs**: Verifique conexões com banco
2. **Frontend Logs**: Verifique build e nginx
3. **System Logs**: Verifique recursos do sistema

### **Health Checks**

O sistema possui health checks automáticos:

- **Backend**: Verifica API e conexão com banco
- **Frontend**: Verifica nginx e arquivos estáticos

### **Métricas**

Monitore no painel do Coolify:

- CPU e Memória
- Rede (conexões com banco)
- Disk I/O
- Uptime

## 🛠️ Troubleshooting

### **Problema: Erro de Conexão com Banco**

```bash
# Verificar conectividade
docker exec -it <backend_container> ping SRVTOTVS02
docker exec -it <backend_container> telnet SRVTOTVS02 1433

# Verificar drivers ODBC
docker exec -it <backend_container> odbcinst -q -d
```

### **Problema: Frontend não Carrega**

```bash
# Verificar arquivos estáticos
docker exec -it <frontend_container> ls -la /usr/share/nginx/html/

# Verificar configuração nginx
docker exec -it <frontend_container> nginx -t
```

### **Problema: Erro 502 Bad Gateway**

1. Verificar se backend está rodando na porta 8000
2. Verificar configuração do proxy nginx
3. Verificar health checks

### **Problema: SSL/TLS**

1. Verificar se domínio aponta para VPS
2. Verificar configuração do Coolify
3. Verificar logs do Traefik

## 🔄 Atualizações

### **Deploy de Nova Versão**

1. Faça push para o repositório Git
2. No Coolify, clique em "Deploy"
3. Aguarde o build e deploy automático

### **Rollback**

1. No painel do Coolify
2. Vá para "Deployments"
3. Selecione versão anterior
4. Clique em "Redeploy"

## 🔐 Segurança

### **Recomendações**

1. **Senhas Fortes**: Use senhas complexas para produção
2. **SSL/TLS**: Sempre use HTTPS em produção
3. **Firewall**: Configure regras restritivas
4. **Backup**: Configure backup automático dos dados
5. **Monitoramento**: Configure alertas para falhas

### **Variáveis Sensíveis**

- Nunca commite senhas no Git
- Use o sistema de secrets do Coolify
- Rotacione senhas periodicamente

## 📊 Performance

### **Otimizações**

1. **Backend**:
   - Use connection pooling para banco
   - Configure workers do Uvicorn
   - Ative compressão gzip

2. **Frontend**:
   - Arquivos estáticos são servidos pelo nginx
   - Compressão automática ativada
   - Cache headers configurados

3. **Banco de Dados**:
   - Use índices apropriados
   - Configure timeout de conexão
   - Monitore queries lentas

## 📞 Suporte

### **Logs Importantes**

```bash
# Logs do backend
docker logs <backend_container>

# Logs do frontend
docker logs <frontend_container>

# Logs do sistema
journalctl -u docker
```

### **Comandos Úteis**

```bash
# Status dos containers
docker ps

# Recursos utilizados
docker stats

# Reiniciar serviço
docker-compose restart backend

# Verificar saúde
curl -f https://sinistros.seudominio.com.br/api/health
```

---

## ✅ Checklist de Deploy

- [ ] VPS configurada com Coolify
- [ ] Domínio configurado e DNS apontando
- [ ] Variáveis de ambiente configuradas
- [ ] Conectividade com bancos de dados testada
- [ ] Primeiro deploy realizado
- [ ] Dados inicializados (usuário admin criado)
- [ ] Health checks funcionando
- [ ] SSL/TLS ativo
- [ ] Login testado
- [ ] Funcionalidades básicas testadas
- [ ] Monitoramento configurado
- [ ] Backup configurado

---

**🎉 Sistema pronto para produção!**

Acesse: `https://sinistros.seudominio.com.br`  
Login: `admin` / `BrSamor@2025!`