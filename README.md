Sistema de Controle de Sinistros
Um sistema completo de gestão de incidentes de transporte, com integração de dados em tempo real e uma interface web moderna.

Visão geral
Esta solução permite o gerenciamento integral de sinistros de transporte, integrando-se diretamente a um banco de dados SQL Server com mais de 8 000 registros reais. A arquitetura combina FastAPI no backend e React no frontend, assegurando alto desempenho e excelente experiência do usuário.

Funcionalidades
Integração de dados em tempo real
Conexão direta ao SQL Server

Mais de 8 000 ocorrências reais

Consultas otimizadas para máximo desempenho

Sincronização instantânea

Interface moderna
Design responsivo com temas claro/escuro

Componentes reutilizáveis e escaláveis

Experiência de usuário aprimorada

Dashboard profissional com métricas em tempo real

Gestão avançada
Filtros avançados e busca inteligente

Exportação de dados (CSV/Excel/PDF)

Paginação eficiente

Ordenação de colunas

Arquitetura
scss
Copiar
Editar
├── Backend (FastAPI + Python)
│   ├── REST API completa
│   ├── Conexão SQL Server
│   ├── Validação com Pydantic
│   └── Documentação automática
│
├── Frontend (React + Vite)
│   ├── React 18 com Hooks
│   ├── Tailwind CSS
│   ├── React Router
│   └── Temas dinâmicos
│
└── Integração
    ├── CORS configurado
    ├── API RESTful
    └── Design responsivo
Início rápido
Instalação automática (recomendado)
bash
Copiar
Editar
# Executa o sistema completo
start_complete_system_ultrathink.bat
Instalação manual
Backend
bash
Copiar
Editar
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Frontend
bash
Copiar
Editar
cd frontend
npm install
npm run dev
Pontos de acesso
Frontend: http://localhost:5173

Documentação da API (Swagger): http://localhost:8000/docs

API ReDoc: http://localhost:8000/redoc

Health Check: http://localhost:8000/health

Stack de tecnologias
Backend
FastAPI – Framework web moderno e rápido

SQLAlchemy – ORM para bancos relacionais

Pydantic – Validação e tipagem de dados

PyODBC – Conexão com SQL Server

Uvicorn – Servidor ASGI

Frontend
React 18 – Biblioteca para interfaces de usuário

Vite – Ferramenta de build ultra-rápida

Tailwind CSS – CSS utilitário

React Router – Roteamento client-side

Context API – Gerenciamento de estado

Esquema de banco de dados
Tabelas principais integradas:

Tabela	Descrição
tbdOcorrenciaNota	Anotações de sinistros
tbdOcorrencia	Tipos de sinistros
tbdMovimento	Movimentações de carga
tbdMovimentoNotaFiscal	Relação movimento × nota fiscal

Tipos de sinistro
Avaria Parcial/Total – Danos à mercadoria

Perda Parcial/Total – Perda de mercadoria

Roubo de Carga – Subtração durante o transporte

Mercadoria Danificada – Casos concluídos

Principais componentes
Dashboard
Métricas em tempo real

Seletor de período (7, 30, 90, 365 dias)

Monitoramento de status da conexão

Visão geral de incidentes recentes

Gestão de dados
Sistema de filtros avançados

Busca inteligente

Paginação otimizada

Tabelas responsivas

Endpoints da API
/api/sinistros – Gestão de ocorrências

/api/dashboard – Métricas para o dashboard

/api/health – Verificação de integridade

/api/docs – Documentação interativa

Estrutura do projeto
bash
Copiar
Editar
sinistros-control/
├── backend/
│   ├── app/
│   │   ├── core/          # Configurações centrais
│   │   ├── models/        # Modelos de banco
│   │   ├── repositories/  # Camada de acesso a dados
│   │   ├── routers/       # Rotas da API
│   │   ├── schemas/       # Schemas Pydantic
│   │   └── services/      # Lógica de negócio
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── contexts/      # Provedores de contexto
│   │   ├── pages/         # Páginas
│   │   ├── services/      # Serviços de API
│   │   └── utils/         # Utilidades
│   └── package.json
└── README.md
Padrões de desenvolvimento
Padrões arquiteturais
Princípios de Clean Architecture

Padrão Repository para acesso a dados

Camada de serviços para regras de negócio

Arquitetura frontend baseada em componentes

Qualidade de código
TypeScript para segurança de tipos

ESLint e Prettier para padronização

Design responsivo

Boas práticas de acessibilidade

Roadmap
Fase 2 – Analytics avançado
 Integração de gráficos interativos

 Geração de relatórios PDF/Excel

 Filtro de datas inteligente

 Dashboards personalizáveis

Fase 3 – Funcionalidades estendidas
 CRUD completo

 Upload de documentos

 Fluxos de aprovação

 Notificações em tempo real

Fase 4 – Segurança & compliance
 Autenticação JWT

 Controle de acesso por perfil

 Trilhas de auditoria completas

 Sistema de backup automatizado

Contribuição
Este projeto segue padrões profissionais de desenvolvimento, com arquitetura limpa, componentes reutilizáveis e desempenho otimizado para ambos os temas.

Licença
Projeto desenvolvido para sistemas profissionais de gestão de sinistros de transporte.

<div align="center">
Sistema Profissional de Gerenciamento de Sinistros de Transporte

Construído com tecnologias modernas para máximo desempenho e excelente experiência de uso.

</div>