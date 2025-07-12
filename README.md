# 🚀 Sistema de Gestão de Sinistros ULTRATHINK

Sistema ultra profissional para gestão completa de sinistros de transporte com dados reais e interface moderna.

## ✨ Características ULTRATHINK

### 🎯 **Dados Reais**
- Conexão direta com banco SQL Server
- Mais de 8.000 registros de sinistros reais
- Query otimizada para performance máxima
- Sincronização em tempo real

### 🎨 **Interface Ultra Profissional**
- Design moderno e responsivo
- Modo escuro/claro com cores otimizadas
- Componentes reutilizáveis e escaláveis
- Experiência de usuário otimizada

### 📊 **Dashboard Avançado**
- Métricas em tempo real
- Cards com cores vibrantes no modo escuro
- Análises de desempenho
- Alertas e notificações

### 🔍 **Gestão Completa**
- Filtros avançados
- Busca inteligente
- Exportação de dados
- Paginação eficiente

## 🏗️ Arquitetura

```
├── 🔧 Backend (FastAPI + Python)
│   ├── 📊 API REST completa
│   ├── 🗄️ Conexão SQL Server
│   ├── 📋 Validação com Pydantic
│   └── 📖 Documentação automática
│
├── 🎨 Frontend (React + Vite)
│   ├── ⚛️ React 18 + Hooks
│   ├── 🎨 Tailwind CSS
│   ├── 🧭 React Router
│   └── 🌙 Tema dinâmico
│
└── 🔗 Integração
    ├── 🌐 CORS configurado
    ├── 🔄 API RESTful
    └── 📱 Design responsivo
```

## 🚀 Início Rápido

### 1. **Inicialização Automática (Recomendado)**
```bash
# Execute o script completo
start_complete_system_ultrathink.bat
```

### 2. **Inicialização Manual**

#### Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend:
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Acesso ao Sistema

- **Frontend**: http://localhost:5173
- **API Swagger**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📋 Funcionalidades Implementadas

### 🎯 **Dashboard Ultra Profissional**
- ✅ Métricas principais (Total, Avarias, Extravios, Roubos, Sinistradas)
- ✅ Cards com cores vibrantes no modo escuro
- ✅ Análise de desempenho
- ✅ Sinistros recentes
- ✅ Status de conexão em tempo real
- ✅ Seletor de período (7, 30, 90, 365 dias)

### 📊 **Gestão de Sinistros**
- ✅ Lista completa com dados reais
- ✅ Filtros avançados (data, cliente, NF, conhecimento)
- ✅ Busca inteligente
- ✅ Paginação otimizada
- ✅ Ordenação por colunas
- ✅ Visualização responsiva
- ✅ Formulários com dropdowns (sem radio buttons)

### 🔧 **Componentes ULTRATHINK**
- ✅ `MetricCard` - Cards de métricas com cores otimizadas
- ✅ `DataTable` - Tabela de dados avançada
- ✅ `LoadingSpinner` - Indicador de carregamento
- ✅ Layout ultra profissional
- ✅ Tema dinâmico (escuro/claro)

### 🗄️ **Backend Robusto**
- ✅ API REST completa
- ✅ Conexão PyODBC otimizada
- ✅ Endpoints especializados
- ✅ Validação com Pydantic
- ✅ Documentação automática
- ✅ CORS configurado

## 📊 Dados da Query

### 🔍 **Query Principal**
A query acessa as seguintes tabelas:
- `tbdOcorrenciaNota` - Ocorrências por nota fiscal
- `tbdOcorrencia` - Tipos de ocorrência
- `tbdMovimento` - Movimentações de carga
- `tbdMovimentoNotaFiscal` - Relação movimento/NF

### 📈 **Tipos de Sinistro**
- **Avaria Parcial/Total** - Danos à mercadoria
- **Extravio Parcial/Total** - Perda de mercadoria
- **Roubo de Carga** - Furto durante transporte
- **Mercadoria Sinistrada** - Casos concluídos

### 🏢 **Dados Capturados**
- Nota Fiscal
- Conhecimento/Minuta
- Remetente e Destinatário
- Datas (coleta, evento, cadastro)
- Tipos e descrições de ocorrência
- Status e referências

## 🎨 Melhorias Recentes

### 🌙 **Modo Escuro Otimizado**
- ✅ Cards com cores vibrantes e melhor contraste
- ✅ Backgrounds com transparência e bordas definidas
- ✅ Ícones com cores temáticas por tipo de sinistro
- ✅ Títulos e valores sempre legíveis

### 🎯 **Interface Limpa**
- ✅ Conversão de radio buttons para dropdowns
- ✅ Layout consistente em todos os formulários
- ✅ Melhor acessibilidade e usabilidade
- ✅ Projeto organizado sem arquivos desnecessários

## 🚀 Próximos Passos

### 📊 **Fase 2 - Analytics Avançado**
- [ ] Gráficos interativos (Chart.js)
- [ ] Relatórios em PDF/Excel
- [ ] Filtros de data inteligentes
- [ ] Dashboards personalizáveis

### 🔄 **Fase 3 - Funcionalidades Expandidas**
- [ ] CRUD completo de sinistros
- [ ] Upload de documentos
- [ ] Workflow de aprovação
- [ ] Notificações em tempo real

### 🛡️ **Fase 4 - Segurança e Compliance**
- [ ] Autenticação JWT
- [ ] Controle de acesso por perfil
- [ ] Auditoria completa
- [ ] Backup automático

## 👥 Desenvolvimento

### 🏗️ **Padrões ULTRATHINK**
- **Arquitetura**: Clean Architecture
- **Componentes**: Reutilizáveis e escaláveis
- **Estado**: Context API + Local State
- **Design**: Mobile-first e responsivo
- **Cores**: Otimizadas para ambos os temas

### 📁 **Estrutura do Projeto**
```
sinistros-control/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── contexts/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
├── shell/
└── README.md
```

## 🏷️ Versão

**ULTRATHINK v2.1** - Sistema otimizado e limpo
- ✅ Cores melhoradas no modo escuro
- ✅ Projeto organizado sem arquivos desnecessários
- ✅ Interface consistente com dropdowns
- ✅ Performance otimizada

---

<div align="center">

**🚀 Sistema de Gestão de Sinistros ULTRATHINK**

*Desenvolvido com ❤️ para gestão profissional de sinistros*

</div>
