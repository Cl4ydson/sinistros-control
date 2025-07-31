# Coolify Deployment Guide

## Prerequisites
- Coolify instance running on your VPS
- Docker and Docker Compose installed
- Git repository accessible by Coolify

## Deployment Steps

### 1. Environment Variables in Coolify
Set these environment variables in your Coolify project:

```env
# SQL Server Configuration
MSSQL_SA_PASSWORD=YourStrong!Passw0rd123
MSSQL_PID=Express
MSSQL_TCP_PORT=1433

# Primary Database Configuration
DB_SERVER=your-database-server
DB_DATABASE=AUTOMACAO_BRSAMOR
DB_USERNAME=sa
DB_PASSWORD=your-database-password

# Transport Database Configuration
DB_TRANSPORT_SERVER=your-transport-server
DB_TRANSPORT_DATABASE=dtbTransporte
DB_TRANSPORT_USERNAME=sa
DB_TRANSPORT_PASSWORD=your-transport-password

# Security Configuration (CHANGE THIS!)
SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://your-domain.com

# SQL Server Connection Configuration
TRUST_SERVER_CERTIFICATE=yes
ENCRYPT=no

# Frontend Configuration
VITE_API_BASE_URL=/api
VITE_DEMO_MODE=false
```

### 2. Coolify Configuration
1. Create a new project in Coolify
2. Set the repository URL
3. **IMPORTANT**: Specify the exact compose file name:
   - `docker-compose.minimal.yml` ⭐⭐ (MOST RECOMMENDED - no health checks, no dependencies)
   - `compose.simple.yaml` ⭐ (no health checks)
   - `compose.yaml` (with health checks - may fail)
4. Configure the environment variables above
5. Set up domain/subdomain for your application

**CRITICAL**: Make sure to specify the exact filename in Coolify's compose file field. Do NOT leave it blank or it will use the wrong file.

### Troubleshooting SQL Server Issues:
- If you see "container sqlserver is unhealthy" → Use `docker-compose.minimal.yml`
- If you see "dependency failed to start" → Use `docker-compose.minimal.yml`
- The minimal version has no health checks and no dependencies between services

### 3. Port Configuration
- Frontend: Port 80 (will be proxied by Coolify)
- Backend: Port 8000 (internal)
- Database: Port 1433 (internal)

### 4. Volume Persistence
Ensure these volumes are persistent:
- `sqlserver_data` - Database files

### 5. Health Checks
The containers include health checks:
- Backend: `GET /health`
- Frontend: `GET /`
- Database: SQL Server connection test

## Troubleshooting

### Common Issues:

1. **Database Connection Errors**
   - Check if SQL Server container is healthy
   - Verify environment variables
   - Check network connectivity between containers

2. **Frontend API Calls Failing**
   - Ensure `VITE_API_BASE_URL=/api`
   - Check nginx proxy configuration
   - Verify CORS settings

3. **Build Failures**
   - Check Dockerfile syntax
   - Verify all required files are in the repository
   - Check build logs in Coolify

4. **Container Startup Issues**
   - Check container logs in Coolify
   - Verify health check endpoints
   - Check resource limits

### Debugging Commands:
```bash
# Check container status
docker ps

# View container logs
docker logs <container_name>

# Execute into container
docker exec -it <container_name> /bin/bash

# Check database connection
docker exec -it sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P <password>
```

## Production Considerations

1. **Security**
   - Change default passwords
   - Use strong SECRET_KEY
   - Enable HTTPS
   - Restrict CORS origins

2. **Performance**
   - Configure appropriate resource limits
   - Set up database backups
   - Monitor container health

3. **Monitoring**
   - Set up log aggregation
   - Configure alerts for container failures
   - Monitor database performance