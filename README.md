# Sinistros Control System

A comprehensive transportation incident management system with real-time data integration and modern web interface.

## Overview

This system provides complete management of transportation incidents with direct SQL Server database integration, featuring over 8,000 real incident records. Built with FastAPI backend and React frontend for optimal performance and user experience.

## Features

### Real-time Data Integration
- Direct SQL Server database connection
- 8,000+ real incident records
- Optimized queries for maximum performance
- Real-time synchronization

### Modern Interface
- Responsive design with dark/light theme support
- Reusable and scalable components
- Optimized user experience
- Professional dashboard with real-time metrics

### Advanced Management
- Advanced filtering and intelligent search
- Data export capabilities
- Efficient pagination
- Column sorting

## Architecture

```
├── Backend (FastAPI + Python)
│   ├── Complete REST API
│   ├── SQL Server connection
│   ├── Pydantic validation
│   └── Automatic documentation
│
├── Frontend (React + Vite)
│   ├── React 18 with Hooks
│   ├── Tailwind CSS
│   ├── React Router
│   └── Dynamic theming
│
└── Integration
    ├── CORS configured
    ├── RESTful API
    └── Responsive design
```

## Quick Start

### Automated Setup (Recommended)
```bash
# Run the complete system
start_complete_system_ultrathink.bat
```

### Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Access Points

- **Frontend**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **PyODBC** - SQL Server connection
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - Frontend framework
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS
- **React Router** - Client-side routing
- **Context API** - State management

## Database Schema

The system integrates with the following database tables:
- `tbdOcorrenciaNota` - Incident notes
- `tbdOcorrencia` - Incident types
- `tbdMovimento` - Cargo movements
- `tbdMovimentoNotaFiscal` - Movement/invoice relationships

### Incident Types
- **Partial/Total Damage** - Merchandise damage
- **Partial/Total Loss** - Merchandise loss
- **Cargo Theft** - Theft during transport
- **Damaged Merchandise** - Concluded cases

## Key Components

### Dashboard
- Real-time metrics display
- Period selector (7, 30, 90, 365 days)
- Connection status monitoring
- Recent incidents overview

### Data Management
- Advanced filtering system
- Intelligent search functionality
- Optimized pagination
- Responsive data tables

### API Endpoints
- `/api/sinistros` - Incident management
- `/api/dashboard` - Dashboard metrics
- `/api/health` - System health check
- `/api/docs` - API documentation

## Project Structure

```
sinistros-control/
├── backend/
│   ├── app/
│   │   ├── core/          # Core configuration
│   │   ├── models/        # Database models
│   │   ├── repositories/  # Data access layer
│   │   ├── routers/       # API routes
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── contexts/      # Context providers
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── utils/         # Utility functions
│   └── package.json
└── README.md
```

## Development Standards

### Architecture Patterns
- Clean Architecture principles
- Repository pattern for data access
- Service layer for business logic
- Component-based frontend architecture

### Code Quality
- TypeScript for type safety
- ESLint and Prettier for code formatting
- Responsive design principles
- Accessibility best practices

## Roadmap

### Phase 2 - Advanced Analytics
- [ ] Interactive charts integration
- [ ] PDF/Excel report generation
- [ ] Intelligent date filtering
- [ ] Customizable dashboards

### Phase 3 - Extended Functionality
- [ ] Complete CRUD operations
- [ ] Document upload system
- [ ] Approval workflows
- [ ] Real-time notifications

### Phase 4 - Security & Compliance
- [ ] JWT authentication
- [ ] Role-based access control
- [ ] Complete audit trail
- [ ] Automated backup system

## Contributing

This project follows professional development standards with clean architecture, reusable components, and optimized performance for both themes.

## License

This project is developed for professional incident management systems.

---

<div align="center">

**Professional Transportation Incident Management System**

*Built with modern technologies for optimal performance and user experience*

</div>
