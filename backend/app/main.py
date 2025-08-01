from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, sinistros, sinistros_automacao_simple

# REMOVIDO: Base.metadata.create_all(bind=engine) 
# As tabelas já existem nos bancos de dados

app = FastAPI(
    title="Sinistros Control API",
    description="API para controle de sinistros",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80", "http://localhost:5173", "http://localhost:3000"],  # URLs do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# plugando as rotas
app.include_router(auth.router)
app.include_router(sinistros.router)
app.include_router(sinistros_automacao_simple.router)

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Sinistros Control API está funcionando",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Health check endpoint for Docker containers"""
    return {
        "status": "healthy",
        "service": "sinistros-backend",
        "version": "1.0.0"
    }

@app.get("/test-db")
def test_database_connection():
    """Testa conexão com o banco de dados"""
    from .database import get_db_principal
    from . import models
    
    try:
        db = next(get_db_principal())
        
        # Testa conexão básica
        from sqlalchemy import text
        result = db.execute(text("SELECT 1 as test")).fetchone()
        
        # Tenta contar usuários na tabela
        user_count = db.query(models.user.User).count()
        
        # Tenta listar alguns usuários (apenas login, sem senha)
        users = db.query(models.user.User.login, models.user.User.nome).limit(5).all()
        
        return {
            "status": "success",
            "database": "AUTOMACAO_BRSAMOR",
            "connection": "OK",
            "test_query": result[0] if result else None,
            "user_count": user_count,
            "sample_users": [{"login": u.login, "nome": u.nome} for u in users]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "database": "AUTOMACAO_BRSAMOR", 
            "error": str(e),
            "error_type": type(e).__name__
        }
