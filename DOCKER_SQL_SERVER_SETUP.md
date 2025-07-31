# Docker SQL Server Setup

This document describes how to run the Sinistros Control application with a containerized SQL Server database.

## Overview

The docker-compose.yml now includes:
- **SQL Server 2022 Express** container
- **Automatic database initialization** with sample data
- **Persistent data storage** using Docker volumes
- **Health checks** to ensure proper startup sequence

## Services

### 1. SQL Server (`sqlserver`)
- **Image**: `mcr.microsoft.com/mssql/server:2022-latest`
- **Port**: `1433:1433`
- **Databases**: `AUTOMACAO_BRSAMOR`, `dtbTransporte`
- **Data Persistence**: Docker volumes for data, logs, and secrets

### 2. SQL Server Initialization (`sqlserver-init`)
- **Purpose**: Runs database initialization scripts
- **Execution**: Runs once after SQL Server is healthy
- **Scripts**: Creates databases, tables, and sample data

### 3. Backend (`backend`)
- **Dependencies**: Waits for SQL Server and initialization to complete
- **Configuration**: Automatically connects to containerized SQL Server

## Quick Start

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/Cl4ydson/sinistros-control.git
   cd sinistros-control
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Customize environment variables** (optional):
   ```env
   MSSQL_SA_PASSWORD=YourStrong!Passw0rd123
   SECRET_KEY=your-production-secret-key
   ```

4. **Start the application**:
   ```bash
   docker-compose up -d
   ```

5. **Check status**:
   ```bash
   docker-compose ps
   docker-compose logs sqlserver
   docker-compose logs sqlserver-init
   docker-compose logs backend
   ```

## Database Access

### Connection Details
- **Server**: `localhost:1433` (from host) or `sqlserver:1433` (from containers)
- **Username**: `sa`
- **Password**: Value from `MSSQL_SA_PASSWORD` environment variable
- **Databases**: 
  - `AUTOMACAO_BRSAMOR` (main application database)
  - `dtbTransporte` (transport database)

### Sample Users
The initialization creates these test users:
- **Username**: `admin`, **Password**: `secret123`
- **Username**: `user`, **Password**: `secret123`

### Using SQL Server Management Studio (SSMS)
1. Server name: `localhost,1433`
2. Authentication: SQL Server Authentication
3. Login: `sa`
4. Password: Your `MSSQL_SA_PASSWORD`

## Database Schema

### AUTOMACAO_BRSAMOR Database

#### users table
```sql
- id (INT, IDENTITY, PRIMARY KEY)
- username (NVARCHAR(50), UNIQUE)
- email (NVARCHAR(100), UNIQUE)
- hashed_password (NVARCHAR(255))
- is_active (BIT)
- created_at (DATETIME2)
- updated_at (DATETIME2)
```

#### sinistros table
```sql
- id (INT, IDENTITY, PRIMARY KEY)
- numero_sinistro (NVARCHAR(50), UNIQUE)
- data_ocorrencia (DATETIME2)
- descricao (NVARCHAR(MAX))
- status (NVARCHAR(50))
- valor_estimado (DECIMAL(18,2))
- segurado (NVARCHAR(100))
- tipo_sinistro (NVARCHAR(50))
- created_at (DATETIME2)
- updated_at (DATETIME2)
- created_by (INT, FK to users.id)
```

### dtbTransporte Database

#### transportes table
```sql
- id (INT, IDENTITY, PRIMARY KEY)
- codigo (NVARCHAR(50), UNIQUE)
- descricao (NVARCHAR(255))
- status (NVARCHAR(50))
- created_at (DATETIME2)
- updated_at (DATETIME2)
```

## Maintenance Commands

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f sqlserver
docker-compose logs -f backend
```

### Restart services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart sqlserver
docker-compose restart backend
```

### Reinitialize database
```bash
# Stop services
docker-compose down

# Remove database volume (WARNING: This deletes all data)
docker volume rm sinistros-sqlserver-data

# Start services (will recreate and initialize database)
docker-compose up -d
```

### Access SQL Server container
```bash
# Connect to SQL Server container
docker exec -it sinistros-sqlserver bash

# Run sqlcmd inside container
docker exec -it sinistros-sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourStrong!Passw0rd
```

## Backup and Restore

### Create backup
```bash
# Connect to SQL Server and create backup
docker exec -it sinistros-sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourStrong!Passw0rd -Q "BACKUP DATABASE AUTOMACAO_BRSAMOR TO DISK = '/var/opt/mssql/data/AUTOMACAO_BRSAMOR.bak'"
```

### Copy backup to host
```bash
docker cp sinistros-sqlserver:/var/opt/mssql/data/AUTOMACAO_BRSAMOR.bak ./backup/
```

## Troubleshooting

### SQL Server not starting
1. Check if port 1433 is available
2. Verify password complexity requirements
3. Check container logs: `docker-compose logs sqlserver`

### Initialization scripts not running
1. Check init container logs: `docker-compose logs sqlserver-init`
2. Verify SQL script syntax
3. Ensure proper file permissions

### Backend connection issues
1. Verify SQL Server is healthy: `docker-compose ps`
2. Check backend environment variables
3. Test connection: `docker-compose exec backend python -c "from app.database import test_connection; test_connection()"`

### Performance optimization
1. Increase SQL Server memory if needed
2. Monitor container resources: `docker stats`
3. Consider using SQL Server Standard instead of Express for production

## Security Notes

1. **Change default passwords** in production
2. **Use strong passwords** (minimum 8 characters, uppercase, lowercase, numbers, symbols)
3. **Limit network access** to SQL Server port in production
4. **Regular backups** are essential
5. **Keep SQL Server image updated**

## Production Considerations

1. **Use SQL Server Standard or Enterprise** for production workloads
2. **Configure proper backup strategy**
3. **Set up monitoring and alerting**
4. **Use external volumes** for better performance
5. **Configure SSL/TLS** for connections
6. **Implement proper access controls**

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `MSSQL_SA_PASSWORD` | `YourStrong!Passw0rd` | SQL Server SA password |
| `MSSQL_PID` | `Express` | SQL Server edition |
| `MSSQL_TCP_PORT` | `1433` | SQL Server port |
| `DB_SERVER` | `sqlserver` | Database server hostname |
| `DB_DATABASE` | `AUTOMACAO_BRSAMOR` | Primary database name |
| `DB_USERNAME` | `sa` | Database username |
| `DB_PASSWORD` | Same as `MSSQL_SA_PASSWORD` | Database password |